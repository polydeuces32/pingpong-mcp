# 🎮 Ping Pong • MCP

A modern, responsive ping pong game built with Pure HTML5 Canvas and FastAPI.

## 🚀 Features

### 🎯 **Core Gameplay**
- **Smooth 60fps gameplay** with Pure HTML5 Canvas
- **Realistic physics** with ball speed increase on hits
- **Multiple game modes**: First to 5, First to 10, Best of 3
- **AI opponent** with 3 difficulty levels (Easy, Medium, Hard)
- **Score tracking** and game timer
- **Pause/Resume** functionality

### 🎨 **Visual Design**
- **Modern UI** with gradients and glow effects
- **Responsive design** that works on desktop and mobile
- **Smooth animations** and visual feedback
- **Professional color scheme** with red, blue, and white accents

### 🏆 **Competitive Features**
- **Player name customization**
- **Persistent score tracking** with SQLite database
- **Leaderboard system** with win rates and statistics
- **Match history** and sats rewards

### ⌨️ **Controls**
- **Left Player**: W (up) / S (down)
- **Right Player**: ↑ (up) / ↓ (down) 
- **Game Controls**: SPACE (pause) / R (reset)

## 🛠️ **Technical Stack**

- **Frontend**: Pure HTML5 Canvas + JavaScript (no external libraries)
- **Backend**: FastAPI + SQLModel
- **Database**: SQLite
- **Styling**: Pure CSS with modern gradients and animations

## 🚀 **Quick Start**

1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlmodel
   ```

2. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Open the game**:
   - Main game: `http://localhost:8000/`
   - Leaderboard: `http://localhost:8000/leaderboard`
   - API: `http://localhost:8000/api/leaderboard`

## 📁 **Project Structure**

```
pingpong-mcp/
├── main.py              # FastAPI server with database models
├── static/
│   ├── index.html       # Main game (Pure Canvas)
│   ├── simple.html      # Alternative simple version
│   ├── css-demo.html    # CSS animation demo
│   ├── debug.html       # Debug tools
│   └── test.html        # Quick test page
├── db.sqlite           # SQLite database
└── README.md           # This file
```

## 🎮 **Game Modes**

- **First to 5**: First player to reach 5 points wins
- **First to 10**: First player to reach 10 points wins  
- **Best of 3**: First player to win 2 games wins the match

## 🤖 **AI Difficulty**

- **Easy**: Slow reaction, high randomness
- **Medium**: Balanced speed and prediction
- **Hard**: Fast reaction, good ball prediction

## 🏆 **Leaderboard**

The leaderboard tracks:
- **Player names**
- **Wins and losses**
- **Win percentage**
- **Total sats earned**

## 🔧 **API Endpoints**

- `GET /` - Main game interface
- `GET /leaderboard` - Leaderboard page
- `GET /api/leaderboard` - Leaderboard JSON data
- `POST /api/match/end` - Save match results

## ✨ **Why Pure Canvas?**

This project uses **Pure HTML5 Canvas** instead of external libraries like p5.js or Matter.js because:

- ✅ **No dependencies** - Nothing to break or conflict
- ✅ **Lightweight** - Much smaller file size
- ✅ **Reliable** - No external library issues
- ✅ **Fast** - Direct canvas manipulation
- ✅ **Maintainable** - Simple, readable code
- ✅ **Compatible** - Works everywhere

## 🎯 **Game Features**

### **Enhanced Physics**
- Ball speed increases slightly on each hit
- Realistic paddle collision angles
- Random bounce variations to prevent boring patterns

### **Visual Effects**
- Glowing ball and paddles
- Gradient backgrounds
- Smooth animations
- Responsive design

### **User Experience**
- Clear game status indicators
- Timer display
- Score animations
- Game over modal
- Mobile-friendly controls

## 🚀 **Performance**

- **60fps** smooth gameplay
- **Responsive** design for all screen sizes
- **Lightweight** - No heavy external libraries
- **Fast loading** - Optimized assets and code

## 🎨 **Design Philosophy**

Inspired by **modern design principles**:
- **Function over form** - Clean, purposeful design
- **Geometric shapes** - Simple rectangles and circles
- **Primary colors** - Red, blue, and white palette
- **Minimalist** - No unnecessary elements
- **Modern** - Contemporary gradients and effects

---

**🎮 Ready to play? Visit `http://localhost:8000/` and start your ping pong journey!**
