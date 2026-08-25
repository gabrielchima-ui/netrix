# NETRIX – Enterprise Network Planning Framework

Production-ready web application for enterprise network design with **role-based access control (RBAC)**.

## Roles

| Role | Label | Capabilities |
|------|--------|--------------|
| **admin** | Administrator | Full access, manage all projects, user management |
| **user** | Network Engineer | Create & manage own projects, generate configs, downloads |
| **viewer** | Viewer | Read-only access to own projects |

## Demo accounts

| Role | Email | Password |
|------|--------|----------|
| admin | `admin@netrix.local` | `Admin@12345` |
| user | `engineer@netrix.local` | `Engineer@123` |
| viewer | `viewer@netrix.local` | `Viewer@123` |

Self-registration creates a standard **user** account.

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open **http://127.0.0.1:5000** and sign in with a demo account.

## Features

- Secure authentication (Flask-Login, hashed passwords)
- Role-based access control with permission catalogue
- Project management (VLSM, IPv4, VLAN, Cisco configs)
- Topology & UML diagrams
- PDF / Word / Excel / CSV exports
- Admin user management panel
- REST API under `/api`, `/projects`, `/admin`

## API (authenticated)

| Method | Endpoint | Permission |
|--------|----------|------------|
| GET/POST | `/projects/` | project.list / project.create |
| GET/PUT/DELETE | `/projects/<id>` | project.view / edit / delete |
| POST | `/projects/<id>/generate` | project.generate |
| GET | `/projects/<id>/download/<type>` | project.download |
| GET | `/admin/users` | admin only |
| POST/PUT/DELETE | `/admin/users[/<id>]` | admin only |
| GET | `/api/users/me` | authenticated |
| GET | `/api/permissions` | authenticated |
| GET | `/api/stats` | stats.view |

## Project structure

```
netrix/
├── app/
│   ├── models/          # User, Project, Department, GeneratedData
│   ├── routes/          # auth, main, projects, api, admin
│   ├── services/        # network_engine, reports
│   ├── utils/rbac.py    # roles, permissions, decorators
│   └── templates/
├── config.py
├── run.py
└── requirements.txt
```

## Production notes

- Set strong `SECRET_KEY` in `.env`
- Use `gunicorn -w 4 -b 0.0.0.0:8000 "run:app"`
- Optional MySQL: `DATABASE_URL=mysql+pymysql://user:pass@host/netrix`
