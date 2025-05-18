# 🚀 Astrocat

**A digital observatory for space researchers**

Astrocat is a Django web application that brings together astronomy enthusiasts and professionals. Publish notes, explore the cosmos, share knowledge, and connect within the community.

---

## 🎯 Project Goals

- **Space for notes** — publish personal observations and research.
- **Cosmic catalog** — an open database of stars, planets, and galaxies.
- **Community** — uniting enthusiasts and professionals.

---

## ✨ Features

- 📝 Publishing notes with text, images, and links.
- 🔍 Searching and editing objects in the astronomical catalog.
- 💬 Discussion of materials (coming soon).

---

## ❤️ Why Astrocat?

The project is created with love for science and the mission to make astronomy knowledge accessible and inspiring. We are open to collaboration and new ideas.

---

## ⚙️ Technologies

- Python 3  
- Minio  
- Django  
- HTML/CSS (Bootstrap 5)  
- PostgreSQL  

---

## 🚀 Running the Project

### Manually

Before running migrations, create the PostgreSQL database and Minio file storage, and configure your `.env` file.

```bash
git clone https://github.com/your-username/astrocat.git
make install
make migrate
make run-server
```

### Using Docker

Before starting, configure your `*.env` files based on the examples.

```bash
git clone https://github.com/your-username/astrocat.git
docker-compose up -d --build
```

---

## 📬 Contacts

- **Email:** [astrocat@example.com](mailto:astrocat@example.com)
- **Telegram:** _Coming soon_
