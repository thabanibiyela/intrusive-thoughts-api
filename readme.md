# Intrusive Thoughts

A social networking API where users — called **thinkers** — post their most intrusive thoughts for others to browse, score, and comment on. The more intrusive, the better.

> Example thoughts posted by user `elonmusk`:
> - *"What if our entire universe is just a simulation running on someone else's computer?"*
> - *"Would people be interested in buying flamethrowers for recreational purposes?"*
> - *"What if I could implant Bluetooth chips in people's brains to connect them to the internet?"*

---

## Overview

Intrusive Thoughts is a REST API built with Node.js and Express, backed by MongoDB. It implements OAuth-style token authentication, role-based access control, and a full suite of CRUD operations across three data models.

**Key concepts:**
- **Thinkers** — registered users
- **Thoughts** — posts made by thinkers
- **Echo chambers** — topic tags (similar to hashtags) that group like-minded thinkers
- **Score** — the equivalent of "likes" on a thought

---

## Tech Stack


| Library | Version | Purpose |
|---|---|---|
| Express | 4.19.1 | Web framework |
| Mongoose | 8.2.2 | MongoDB ODM |
| JSON Web Token | 9.0.2 | OAuth token authentication |
| Bcryptjs | 2.4.3 | Password hashing |
| JOI | 17.12.2 | Schema validation |
| Body-Parser | 1.20.2 | Request body parsing |
| Dotenv | 16.4.5 | Environment variable management |
| Nodemon | 3.1.0 | Dev server auto-restart |
| Requests (Python) | 2.31.0 | HTTP requests in test suite |

---

## Data Models

### Thinker

| Field | Type | Validation | Description |
|---|---|---|---|
| username | String | 4–12 characters | Unique application username |
| email | String | Valid email, 4–320 chars | Unique email address |
| password | String | 6–32 characters | Hashed on storage |
| firstName | String | 1–32 characters | First name |
| lastName | String | 1–32 characters | Last name |
| dateJoined | Date | — | Set automatically on registration |
| echoChambers | [String] | Array | Topic interests for the thinker |
| role | String | — | `user` or `admin`, set on registration |

### Thought

| Field | Type | Validation | Description |
|---|---|---|---|
| title | String | 4–75 characters | Short title |
| description | String | 4–140 characters | Brief description |
| detail | String | 4–800 characters | Full content |
| echoChamber | String | 1–32 characters | Topic tag for the thought |
| image | String | Valid URL | Optional image or resource link |
| thinker | ObjectId | — | Author's ID, set automatically |
| timestamp | Date | — | Set automatically on posting |
| score | Number | — | Accumulated scores from other thinkers |
| comments | [ObjectId] | — | References to comment documents |

### Comment

| Field | Type | Validation | Description |
|---|---|---|---|
| detail | String | 4–400 characters | Comment content |
| thinker | ObjectId | — | Author's ID, set automatically |
| timestamp | Date | — | Set automatically on posting |

---

## Admin Tools

Users registered with the correct `admin_secret` header receive the `admin` role, which grants:

- Delete any thinker's account or thoughts (not just their own)
- Bulk-delete all thinkers or all thoughts via a single request
- Access to parallel test databases (isolated from live data)

---

## Running the API

Install dependencies:

```bash
npm install
```

Start the server:

```bash
npm start
```

Expected output:

```
[nodemon] 3.1.0
[nodemon] starting `node src/app.js`
{ message: 'Your mongoDB connector is on...' }
{ message: 'Your server is up and running...' }
```

The API root is available at `http://localhost:3000`.

![API root](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.002.png)

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/register` | — | Register a new thinker. Pass `admin_secret` header for admin role. |
| POST | `/signin` | — | Sign in and receive an auth token. |
| POST | `/thoughts` | Required | Post a new thought. |
| PATCH | `/thoughts/comment/:thoughtId` | Required | Comment on a thought. |
| PATCH | `/thoughts/like/:thoughtId` | Required | Score (like) a thought. |
| GET | `/thinkers` | Required | Browse all thinkers. |
| GET | `/thoughts` | Required | Browse all thoughts. |
| GET | `/thinkers/:lookupValue` | Required | Get a thinker by ID, username, or email. |
| GET | `/thoughts/:thoughtId` | Required | Get a thought by ID. |
| GET | `/thoughts/:thoughtId/comments` | Required | Browse comments on a thought. |
| DELETE | `/thoughts/:thoughtId` | Required | Delete a thought (admin can delete any). |
| DELETE | `/thinkers/:lookupValue` | Required | Delete an account (admin can delete any). |

> All authenticated requests require an `auth_token` header. Obtain it from the `/signin` response.  
> Pass `test_flag=TRUE` to route requests to the test database (admin only).

### Screenshots

| # | Endpoint | Screenshot |
|---|---|---|
| 001 | Register new thinker | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.003.png) |
| 002 | Sign in | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.004.png) |
| 003 | Post a thought | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.005.png) |
| 004 | Comment on a thought | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.006.png) |
| 005 | Score a thought | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.007.png) |
| 006 | Browse all thinkers | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.008.png) |
| 007 | Browse all thoughts | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.009.png) |
| 008 | Get thinker by ID/username/email | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.010.png) |
| 009 | Get thought by ID | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.011.png) |
| 010 | Browse comments on a thought | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.012.png) |
| 011 | Delete a thought | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.013.png) |
| 012 | Delete a thinker account | ![](assets/Aspose.Words.ee17eec8-d6d3-4e6e-a02c-aa30d277b40a.014.png) |

---

## Testing

Tests are written in Python using the `unittest` framework. `test/app.py` acts as a bridge to the API endpoints, and `test/test_app.py` contains 21 standalone test cases covering the full functional spec. Each test is independent and can be run individually or all at once.

Run from the `test/` directory:

```bash
python3 test_app.py
```

Results are written to `test/test_reports/testing.out`. All 21 tests pass.

### Test Cases

| # | ID | Detail | Result |
|---|---|---|---|
| 1 | TC01-Mary | Olga, Nick and Mary register and access the API. | ✅ |
| 2 | TC01 | Test user can access the API root (no auth required). | ✅ |
| 3 | TC01-Nick | Olga, Nick and Mary register and access the API. | ✅ |
| 4 | TC01-Olga | Olga, Nick and Mary register and access the API. | ✅ |
| 5 | TC02-Mary | Olga, Nick and Mary get their auth tokens via OAuth. | ✅ |
| 6 | TC02-Nick | Olga, Nick and Mary get their auth tokens via OAuth. | ✅ |
| 7 | TC02-Olga | Olga, Nick and Mary get their auth tokens via OAuth. | ✅ |
| 8 | TC03 | Olga calls a protected endpoint without a token — should fail. | ✅ |
| 9 | TC04-Olga | Olga posts a thought using her token. | ✅ |
| 10 | TC05-Nick | Nick posts a thought using his token. | ✅ |
| 11 | TC06-Mary | Mary posts a thought using her token. | ✅ |
| 12 | TC07-Nick | Nick browses all thoughts in reverse chronological order. | ✅ |
| 13 | TC07-Olga | Olga browses all thoughts in reverse chronological order. | ✅ |
| 14 | TC08 | Nick and Olga comment on Mary's thought in round-robin. | ✅ |
| 15 | TC09-Mary | Mary comments her own thought — should fail. | ✅ |
| 16 | TC10-Mary | Mary sees thoughts in reverse chronological order. | ✅ |
| 17 | TC11-Mary | Mary views the comments on her thought. | ✅ |
| 18 | TC12 | Nick and Olga score Mary's thought. | ✅ |
| 19 | TC13-Mary | Mary scores her own thought — should fail. | ✅ |
| 20 | TC14-Mary | Mary sees her thought now has two scores. | ✅ |
| 21 | TC15-Nick | Nick sees Mary's thought at the top due to its score. | ✅ |
