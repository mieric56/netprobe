# NetProbe — PingPlotter-style Network Monitor

A self-contained Docker app that replicates PingPlotter's core functionality: continuous ICMP ping monitoring, hop-by-hop MTR/traceroute, historical data browsing, and alert notifications — all through a web dashboard.

## Features

- **Continuous ICMP Ping** — Per-target probing with configurable intervals (1s to 5m)
- **Hop-by-hop MTR** — On-demand MTR with full hop statistics (loss, avg, best, worst, stdev)
- **Traceroute** — On-demand traceroute with per-hop RTT data
- **PingPlotter-style Timeline** — Color-coded latency/loss/jitter strips
- **Interactive Charts** — Zoomable line charts for latency, packet loss, and jitter
- **History Browsing** — Browse 5m to 7d of ping history per target
- **Threshold Alerts** — RTT, packet loss, or jitter alerts with webhook notifications
- **Teams/Slack/Generic Webhooks** — Auto-detects webhook type and formats accordingly
- **CSV/JSON Export** — Download ping data for any time range
- **Dark Theme Dashboard** — Professional NMS-style web interface
- **Single Container** — One `docker run` command, no external dependencies

## Quick Start

```bash
# Clone or unzip
cd netprobe

# Build and run
docker-compose up -d --build

# Open dashboard
http://<your-server-ip>:8000
```

Or without Docker Compose:

```bash
docker build -t netprobe .
docker run -d \
  --name netprobe \
  --cap-add NET_RAW \
  -p 8000:8000 \
  -v netprobe-data:/data \
  --restart unless-stopped \
  netprobe
```

## Usage

1. Open `http://localhost:8000` in your browser
2. Click **Add Target** and enter a name + host/IP
3. Set the poll interval (1s, 5s, 10s, 30s, 1m, 5m)
4. The dashboard shows live status for all targets
5. Click any target for detailed view with:
   - **Timeline** — PingPlotter-style color bars
   - **Charts** — Line charts with zoom
   - **MTR** — Run on-demand MTR
   - **Traceroute** — Run on-demand traceroute
6. Go to **Alerts** to set threshold-based notifications

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/targets` | List all targets |
| POST | `/api/targets` | Add target `{name, host, poll_interval_sec}` |
| PUT | `/api/targets/:id` | Update target |
| DELETE | `/api/targets/:id` | Delete target + all data |
| GET | `/api/targets/:id/ping?minutes=60` | Ping history |
| GET | `/api/targets/:id/ping/summary?minutes=60` | Stats summary |
| POST | `/api/mtr` | Run MTR `{host, count, max_hops}` |
| GET | `/api/targets/:id/mtr?limit=20` | MTR history |
| POST | `/api/traceroute` | Run traceroute `{host, max_hops}` |
| GET | `/api/targets/:id/traceroute?limit=20` | Traceroute history |
| GET | `/api/alerts` | List alert rules |
| POST | `/api/alerts` | Create alert rule |
| PUT | `/api/alerts/:id` | Update alert |
| DELETE | `/api/alerts/:id` | Delete alert |
| GET | `/api/alerts/history` | Alert event history |
| GET | `/api/dashboard` | Dashboard summary |
| GET | `/api/targets/:id/export?format=csv` | Export data |
| WS | `/ws` | Live ping WebSocket |

## Architecture

```
┌──────────────────────────────────────────────┐
│              Docker Container                 │
│                                              │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │  Frontend    │  │  FastAPI Backend      │  │
│  │  (HTML/CSS/  │  │  ┌────────────────┐  │  │
│  │   Chart.js)  │  │  │ Probe Engine   │  │  │
│  │             ◄──┤  │  (ICMP/MTR/TR)  │  │  │
│  │  Port 8000   │  │  └────────────────┘  │  │
│  └─────────────┘  │  ┌────────────────┐  │  │
│                    │  │ Alert Engine   │  │  │
│                    │  │  (eval + hook) │  │  │
│                    │  └────────────────┘  │  │
│                    │  ┌────────────────┐  │  │
│                    │  │ SQLite + WAL   │  │  │
│                    │  │  /data/        │  │  │
│                    │  └────────────────┘  │  │
│                    └──────────────────────┘  │
└──────────────────────────────────────────────┘
```

## Configuration

| Env Variable | Default | Description |
|---|---|---|
| `PORT` | `8000` | Web UI + API port |
| `NETPROBE_DB` | `/data/netprobe.db` | SQLite database path |

## Requirements

- Docker with `NET_RAW` capability (for ICMP)
- No external DB needed (SQLite bundled)
- ~50MB image size

## Updating

```bash
docker-compose down
docker-compose up -d --build
```

Data persists in the `netprobe-data` volume across rebuilds.
