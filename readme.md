Real-Time Multi-Trader Collaboration Room

A backend-focused real-time trading collaboration platform where traders can join dedicated discussion rooms based on financial assets such as BTC, AAPL, and other supported assets.

The project demonstrates how to build a production-style backend using Django, Django REST Framework, WebSockets, Redis, PostgreSQL, JWT Authentication, and Django Channels.

🚀 Project Overview

The platform allows authenticated users to:

Create trading rooms for supported assets.
Join and leave public trading rooms.
View room details and members.
Participate in real-time discussions.
Send messages through WebSockets.
Store messages permanently in PostgreSQL.
Broadcast messages to all connected users through Redis.
Control WebSocket access using room membership.
Assign roles such as OWNER, MODERATOR, and MEMBER.
Example

A trader can join:

#BTC

and participate in a live conversation:

admin: BTC looks bullish
trader2: Volume is increasing
trader3: Resistance around 120K

All connected members receive messages in real time.

🏗️ Architecture
                         Client
                           │
                           │
                  ┌────────┴────────┐
                  │                 │
             REST API          WebSocket
                  │                 │
                  ▼                 ▼
          Django REST API    Django Channels
                  │                 │
                  │                 ▼
                  │              Redis
                  │                 │
                  ▼                 ▼
              PostgreSQL      Channel Layer
                  │                 │
                  └────────┬────────┘
                           │
                           ▼
                     Trading Rooms
🛠️ Technology Stack
Backend
Python
Django
Django REST Framework
Django Channels
Authentication
JWT Authentication
Database
PostgreSQL
Real-Time Communication
WebSockets
Django Channels
Redis
channels_redis
Infrastructure
Docker
Docker Compose
API Testing
Postman
📂 Core Application Structure
traderoom/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── ...
│
├── rooms/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── chat/
│   ├── consumers.py
│   ├── middleware.py
│   ├── routing.py
│   ├── models.py
│   └── ...
│
├── manage.py
└── README.md
🔐 Authentication Flow

The application uses JWT-based authentication.

User
 │
 ▼
Login API
 │
 ▼
JWT Access Token
 │
 ├──────────────► REST APIs
 │
 └──────────────► WebSocket
                       │
                       ▼
                 Authentication
                       │
                       ▼
                Room Membership
                       │
                       ▼
                  WebSocket

Users must be authenticated before accessing protected APIs or participating in a trading room.

🏠 Trading Room System

Each trading room is associated with a specific asset.

Examples:

#BTC
#AAPL
#ETH

The relationship is:

Asset
  │
  │ One-to-One
  ▼
Room
  │
  │ One-to-Many
  ▼
RoomMember
📊 Asset Model

Assets represent supported financial instruments.

Each asset contains:

symbol
name
asset_type
is_active
created_at

Supported asset types currently include:

STOCK
CRYPTO

Example:

{
    "symbol": "BTC",
    "name": "Bitcoin",
    "asset_type": "CRYPTO",
    "is_active": true
}
🏠 Room Model

A room represents a discussion space associated with an asset.

Room fields include:

name
slug
description
asset
is_public
created_by
created_at

Example:

Asset: BTC
Room: #BTC
Slug: btc

Each asset can have one associated trading room.

👥 Room Membership

Users become members of rooms through the membership system.

Each membership contains:

User
Room
Role
Joined timestamp

Available roles:

OWNER
MODERATOR
MEMBER
Membership relationship
User
 │
 ├── #BTC
 │     └── OWNER
 │
 ├── #AAPL
 │     └── MEMBER
 │
 └── #ETH
       └── MODERATOR

A unique constraint prevents the same user from becoming a member of the same room multiple times.

🔑 Room Authorization

WebSocket access is protected by both:

JWT authentication
Room membership

The connection flow is:

WebSocket Request
       │
       ▼
JWT Authentication
       │
       ├── Invalid → Reject
       │
       ▼
Authenticated User
       │
       ▼
Check Room Membership
       │
       ├── Not a member → Reject
       │
       ▼
Room Member
       │
       ▼
Join Redis Channel Group
       │
       ▼
Accept WebSocket

This prevents an authenticated user from accessing a room simply by knowing its room ID.

🌐 REST API Endpoints

Base URL:

http://127.0.0.1:8000/api/

Protected endpoints require:

Authorization: Bearer <ACCESS_TOKEN>
1. List Assets
Endpoint
GET /api/rooms/assets/
Description

Returns all active assets available for trading rooms.

Example Response
[
    {
        "id": 1,
        "symbol": "BTC",
        "name": "Bitcoin",
        "asset_type": "CRYPTO",
        "is_active": true
    }
]
2. List Trading Rooms
Endpoint
GET /api/rooms/
Description

Returns all public trading rooms.

Rooms are fetched together with their associated asset and creator information.

Example Response
[
    {
        "id": 1,
        "name": "#BTC",
        "slug": "btc",
        "description": "Bitcoin trading discussion",
        "asset": {
            "id": 1,
            "symbol": "BTC",
            "name": "Bitcoin",
            "asset_type": "CRYPTO",
            "is_active": true
        },
        "is_public": true,
        "member_count": 1,
        "created_at": "2026-08-17T03:00:00Z"
    }
]
3. Create Trading Room
Endpoint
POST /api/rooms/
Description

Creates a new trading room for an active asset.

The authenticated user automatically becomes the OWNER of the newly created room.

Request
{
    "symbol": "AAPL",
    "name": "#AAPL",
    "description": "Live discussion for Apple stock"
}
Response
{
    "id": 2,
    "name": "#AAPL",
    "slug": "aapl",
    "description": "Live discussion for Apple stock",
    "asset": {
        "id": 2,
        "symbol": "AAPL",
        "name": "Apple",
        "asset_type": "STOCK",
        "is_active": true
    },
    "is_public": true,
    "member_count": 1,
    "created_at": "2026-08-17T03:10:00Z"
}
Behavior
Authenticated User
       │
       ▼
Create Room
       │
       ▼
Create OWNER Membership
       │
       ▼
Return Room

A room cannot be created if another room already exists for the selected asset.

4. Get Room Details
Endpoint
GET /api/rooms/<room_id>/
Example
GET /api/rooms/1/
Description

Returns details of a specific trading room.

5. Join Trading Room
Endpoint
POST /api/rooms/<room_id>/join/
Example
POST /api/rooms/1/join/
Description

Allows an authenticated user to join a trading room.

The user receives the default role:

MEMBER
Response
{
    "message": "Joined room successfully",
    "membership": {
        "id": 5,
        "username": "trader2",
        "role": "MEMBER",
        "joined_at": "2026-08-17T03:20:00Z"
    }
}

If the user is already a member:

{
    "message": "You are already a member of this room."
}
6. Leave Trading Room
Endpoint
POST /api/rooms/<room_id>/leave/
Example
POST /api/rooms/1/leave/
Description

Allows a member to leave a trading room.

The room owner cannot leave the room.

Owner Protection
OWNER
  │
  └── Cannot leave room

This prevents a room from being left without its owner.

7. List Room Members
Endpoint
GET /api/rooms/<room_id>/members/
Example
GET /api/rooms/1/members/
Description

Returns all members of a trading room.

Example Response
[
    {
        "id": 1,
        "username": "admin",
        "role": "OWNER",
        "joined_at": "2026-08-17T03:00:00Z"
    },
    {
        "id": 2,
        "username": "trader2",
        "role": "MEMBER",
        "joined_at": "2026-08-17T03:15:00Z"
    }
]
🔌 WebSocket API

WebSocket endpoint:

ws://127.0.0.1:8000/ws/chat/<room_id>/?token=<ACCESS_TOKEN>
Example
ws://127.0.0.1:8000/ws/chat/1/?token=YOUR_ACCESS_TOKEN
💬 WebSocket Connection Flow
Client
  │
  │ WebSocket Connection
  ▼
/ws/chat/1/
  │
  ▼
JWT Authentication
  │
  ▼
Check Room Membership
  │
  ▼
Join Redis Group
  │
  ▼
WebSocket Connected

For room 1:

room_1

is used as the Redis channel group.

📤 Sending a Message
Request
{
    "message": "BTC looks bullish"
}
Internal Flow
WebSocket Client
       │
       ▼
ChatConsumer.receive()
       │
       ▼
Validate Message
       │
       ▼
Save Message
       │
       ▼
PostgreSQL
       │
       ▼
Redis Channel Layer
       │
       ▼
Broadcast to Room
       │
       ├── User 1
       ├── User 2
       ├── User 3
       └── User N
📥 WebSocket Response

Example:

{
    "message": "BTC looks bullish",
    "username": "admin",
    "created_at": "2026-08-17T03:32:08.072013+00:00"
}

Every connected member of the room receives the broadcast.

⚡ Real-Time Messaging Architecture

The real-time message pipeline is:

                    WebSocket
                        │
                        ▼
                 ChatConsumer
                        │
                        ▼
                 Save Message
                        │
                        ▼
                   PostgreSQL
                        │
                        │
                        ▼
                  group_send()
                        │
                        ▼
                     Redis
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
           User 1     User 2     User 3
🗄️ Database Relationships
User
 │
 ├───────────────┐
 │               │
 ▼               ▼
RoomMember     Room
 │               │
 │               ├── Asset
 │               │
 │               └── created_by → User
 │
 └── user → User




Room
 │
 └── Messages
       │
       └── user → User
🧠 Redis Usage

Redis is used as the Django Channels channel layer.

Configuration:

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                {
                    "address": "redis://127.0.0.1:6379",
                    "socket_timeout": None,
                    "socket_connect_timeout": 5,
                }
            ],
        },
    },
}

Redis is responsible for passing real-time events between WebSocket connections.

It is not the permanent message database.

Permanent messages are stored in PostgreSQL.

🐘 PostgreSQL Usage

PostgreSQL stores persistent application data such as:

Users
Assets
Trading rooms
Room memberships
Chat messages

This ensures that chat messages remain available after a WebSocket connection closes.

🔄 Complete User Flow

The complete application flow is:

1. User registers/logs in
          │
          ▼
2. User receives JWT access token
          │
          ▼
3. User requests available assets
          │
          ▼
4. User views trading rooms
          │
          ▼
5. User joins a room
          │
          ▼
6. Membership is created
          │
          ▼
7. User opens WebSocket connection
          │
          ▼
8. JWT authentication is validated
          │
          ▼
9. Room membership is validated
          │
          ▼
10. User joins Redis channel group
          │
          ▼
11. User sends trading message
          │
          ▼
12. Message is saved in PostgreSQL
          │
          ▼
13. Redis broadcasts message
          │
          ▼
14. All connected room members receive it
🔒 Security & Validation

The current implementation includes:

JWT authentication
Authenticated REST endpoints
WebSocket authentication
Room membership validation
Unique room membership constraint
Unique asset symbols
One room per asset
Owner role assignment
Owner leave protection
Active asset validation
Empty message validation
Public room filtering
🧪 Current Testing

The following components have been tested successfully:

Redis
Redis PING → PONG
Redis Channel Layer
GROUP ADD → OK
GROUP DISCARD → OK
WebSocket
WebSocket CONNECT → SUCCESS
Message Send → SUCCESS
Message Broadcast → SUCCESS
Message Persistence → SUCCESS
Example Successful Message
{
    "message": "BTC looks bullish",
    "username": "admin",
    "created_at": "2026-08-17T03:32:08.072013+00:00"
}
📋 API Summary
Method	Endpoint	Description
GET	/api/rooms/assets/	List active assets
GET	/api/rooms/	List public rooms
POST	/api/rooms/	Create a trading room
GET	/api/rooms/<room_id>/	Get room details
POST	/api/rooms/<room_id>/join/	Join a room
POST	/api/rooms/<room_id>/leave/	Leave a room
GET	/api/rooms/<room_id>/members/	List room members
WS	/ws/chat/<room_id>/?token=<JWT>	Real-time room chat
🎯 Current Project Status
Django Project Setup              ✅
PostgreSQL                        ✅
JWT Authentication                ✅
Asset Management                  ✅
Trading Rooms                     ✅
Room Membership                   ✅
Room Roles                        ✅
REST Room APIs                    ✅
WebSocket Chat                    ✅
Redis Channel Layer               ✅
Message Persistence               ✅
Room Authorization                ✅
🚧 Upcoming Features

The next development phases will include:

 Chat message history API
 Pagination for messages
 Redis caching
 Celery background tasks
 Market price updates
 Background market-data processing
 Notifications
 Online/offline trader presence
 Moderator functionality
 Message editing/deletion
 Rate limiting
 Automated tests
 Docker production configuration
 API documentation
 Deployment
 Monitoring and logging
💡 Project Goal

The goal of this project is to demonstrate a real-time, scalable backend architecture rather than a basic CRUD application.

It combines:

Django
   +
Django REST Framework
   +
JWT Authentication
   +
PostgreSQL
   +
Redis
   +
Django Channels
   +
WebSockets
   +
Celery
   +
Docker

into a single enterprise-style backend project focused on real-time trader collaboration.