from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Field, Session, SQLModel, create_engine, select
import datetime

# ----------------------------
# ⚙️ Database Models
# ----------------------------
class Player(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    total_wins: int = 0
    total_losses: int = 0
    total_sats_won: int = 0


class Match(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    player1_id: int | None = None
    player2_id: int | None = None
    winner_id: int | None = None
    start_time: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    end_time: datetime.datetime | None = None
    total_points_p1: int = 0
    total_points_p2: int = 0
    sats_reward: int = 0


# ----------------------------
# 🗄️ Database Setup
# ----------------------------
sqlite_file_name = "db.sqlite"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ----------------------------
# 🚀 FastAPI App
# ----------------------------
app = FastAPI(title="Ping Pong MCP Server")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main Ping Pong game."""
    return FileResponse("static/index.html")


# ----------------------------
# 🎮 API Endpoints
# ----------------------------
@app.post("/api/match/end")
async def end_match(match: dict):
    """Save match result to DB and update player stats."""
    try:
        with Session(engine) as session:
            winner = match.get("winner_id")
            p1, p2 = match.get("player1_id", 1), match.get("player2_id", 2)
            points_p1, points_p2 = match.get("points_p1", 0), match.get("points_p2", 0)
            sats_reward = match.get("sats_reward", 0)

            # Create players if they don't exist
            p1_name = match.get("player1_name", "Player1")
            p2_name = match.get("player2_name", "AI")
            
            for pid, name in [(p1, p1_name), (p2, p2_name)]:
                player = session.get(Player, pid)
                if not player:
                    player = Player(id=pid, username=name)
                    session.add(player)
                else:
                    # Update name if it changed
                    player.username = name

            # Record match
            new_match = Match(
                player1_id=p1,
                player2_id=p2,
                winner_id=winner,
                total_points_p1=points_p1,
                total_points_p2=points_p2,
                sats_reward=sats_reward,
                end_time=datetime.datetime.utcnow(),
            )
            session.add(new_match)

            # Update stats
            winner_player = session.get(Player, winner)
            loser_player = session.get(Player, p1 if winner == p2 else p2)
            if winner_player:
                winner_player.total_wins += 1
                winner_player.total_sats_won += sats_reward
            if loser_player:
                loser_player.total_losses += 1

            session.commit()
            session.refresh(new_match)
            return {"message": "Match saved", "match_id": new_match.id}
    except Exception as e:
        print(f"Error saving match: {e}")
        return {"error": "Failed to save match", "details": str(e)}


@app.get("/api/leaderboard")
async def leaderboard():
    """Get the current leaderboard."""
    try:
        with Session(engine) as session:
            players = session.exec(select(Player).order_by(Player.total_wins.desc())).all()
            return [{"username": p.username, "wins": p.total_wins, "losses": p.total_losses, "sats": p.total_sats_won} for p in players]
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return {"error": "Failed to fetch leaderboard", "details": str(e)}


@app.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard_page():
    """Serve the leaderboard page."""
    try:
        with Session(engine) as session:
            players = session.exec(select(Player).order_by(Player.total_wins.desc())).all()
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Ping Pong Leaderboard</title>
                <style>
                    body { background: #1a1a1a; color: white; font-family: Arial; padding: 20px; }
                    h1 { color: #e63946; text-align: center; }
                    table { width: 100%; max-width: 800px; margin: 0 auto; border-collapse: collapse; }
                    th, td { padding: 15px; text-align: left; border-bottom: 1px solid #333; }
                    th { background: #457b9d; color: white; }
                    tr:hover { background: #333; }
                    .rank { font-weight: bold; color: #e63946; }
                    .wins { color: #51cf66; }
                    .losses { color: #ff6b6b; }
                    .sats { color: #ffd43b; }
                    a { color: #457b9d; text-decoration: none; }
                    a:hover { color: #6c9bd1; }
                </style>
            </head>
            <body>
                <h1>🏆 Ping Pong Leaderboard</h1>
                <p style="text-align: center;"><a href="/">← Back to Game</a></p>
                <table>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Wins</th>
                        <th>Losses</th>
                        <th>Win Rate</th>
                        <th>Sats Won</th>
                    </tr>
            """
            
            for i, player in enumerate(players, 1):
                total_games = player.total_wins + player.total_losses
                win_rate = (player.total_wins / total_games * 100) if total_games > 0 else 0
                
                html_content += f"""
                    <tr>
                        <td class="rank">#{i}</td>
                        <td>{player.username}</td>
                        <td class="wins">{player.total_wins}</td>
                        <td class="losses">{player.total_losses}</td>
                        <td>{win_rate:.1f}%</td>
                        <td class="sats">{player.total_sats_won}</td>
                    </tr>
                """
            
            html_content += """
                </table>
                <p style="text-align: center; margin-top: 30px;">
                    <a href="/">Play Ping Pong</a> | 
                    <a href="/api/leaderboard">JSON Data</a>
                </p>
            </body>
            </html>
            """
            
            return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading leaderboard</h1><p>{str(e)}</p>", status_code=500)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("✅ MCP Ping Pong Server running with SQLite")

