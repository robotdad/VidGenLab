from __future__ import annotations

import json
import pathlib

import streamlit as st

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "out"
RATINGS = OUT / "ratings.json"


def load_results() -> list[pathlib.Path]:
    return sorted(p for p in OUT.glob("*.mp4"))


def load_ratings() -> dict[str, int]:
    if RATINGS.exists():
        return json.loads(RATINGS.read_text(encoding="utf-8"))
    return {}


def save_ratings(data: dict[str, int]):
    OUT.mkdir(parents=True, exist_ok=True)
    RATINGS.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main():
    st.set_page_config(page_title="Veo3 A/B Viewer", layout="wide")
    st.title("Veo3 A/B Viewer")
    videos = load_results()
    ratings = load_ratings()
    cols = st.columns(3)
    for i, vid in enumerate(videos):
        with cols[i % 3]:
            st.video(str(vid))
            key = vid.name
            score = ratings.get(key, 0)
            c1, c2, c3 = st.columns(3)
            if c1.button("👍", key=f"up-{key}"):
                ratings[key] = score + 1
            if c2.button("👎", key=f"down-{key}"):
                ratings[key] = score - 1
            if c3.button("reset", key=f"reset-{key}"):
                ratings[key] = 0
            st.caption(f"{key} — score: {ratings.get(key, 0)}")
    if st.button("Save ratings"):
        save_ratings(ratings)
        st.success(f"Saved to {RATINGS}")


if __name__ == "__main__":
    main()
