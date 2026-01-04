# Rock Paper Scissors - System Architecture

This document details the architecture of the **RPS Arena**, a realtime multiplayer gaming platform.

## 1. Overview
RPS Arena is a Full-Stack realtime web application. It enables users to play Rock-Paper-Scissors against the computer or other players online. It features live matchmaking, leaderboards, and persistent player statistics.

## 2. Technical Stack
### Frontend
*   **Framework**: React.js (Vite)
*   **Realtime Client**: `socket.io-client`
*   **Styling**: Tailwind CSS + Framer Motion (Animations)
*   **Auth**: Firebase Auth

### Backend
*   **Server**: Flask (Python) with `flask-socketio`
*   **Concurrency**: Eventlet / Threading (for Socket.IO)
*   **Database**: MongoDB (`rock_paper_scissors` db)
    - Collections: `users`, `games`, `leaderboard`

## 3. Realtime Architecture

```mermaid
sequenceDiagram
    participant Player1
    participant Server
    participant Player2
    participant DB as MongoDB

    Note over Player1, Player2: Matchmaking Phase
    Player1->>Server: emit('join_matchmaking')
    Player2->>Server: emit('join_matchmaking')
    Server->>Server: Match Players()
    Server->>DB: Create Game Record
    Server-->>Player1: emit('game_found')
    Server-->>Player2: emit('game_found')

    Note over Player1, Player2: Gameplay Phase
    Player1->>Server: emit('submit_move', {move: 'rock'})
    Server-->>Player1: Acknowledge Move (Waiting...)
    
    Player2->>Server: emit('submit_move', {move: 'scissors'})
    
    Server->>Server: Resolve Round (Rock beats Scissors)
    Server->>DB: Update Game & Stats
    
    Server-->>Player1: emit('round_result', {win: true})
    Server-->>Player2: emit('round_result', {win: false})
```

## 4. System Component Diagram

```mermaid
graph LR
    Client[React Frontend]
    
    subgraph Interfaces
        WS[Socket.IO]
        HTTP[REST API]
    end
    
    subgraph Backend ["Backend (Flask)"]
        SocketHandler[Socket Handlers]
        Auth[Auth Middleware]
    end
    
    DB[(MongoDB)]
    
    Client --> WS
    Client --> HTTP
    
    WS --> SocketHandler
    HTTP --> Auth
    
    SocketHandler --> DB
    Auth --> DB
```