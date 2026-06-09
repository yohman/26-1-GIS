#!/usr/bin/env python3
# create_groups_worldcup.py
#
# Creates constrained groups from merged_roster_attendance.csv and exports:
# 1. groups_output.csv
# 2. groups_worldcup.html
#
# Usage:
# python create_groups_worldcup.py
# python create_groups_worldcup.py --seed 2026
# python create_groups_worldcup.py --input merged_roster_attendance.csv --group-size 4

import argparse
import math
import random
import csv
import json
from pathlib import Path

COUNTRIES = [
    ("Japan", "JPN", "#D00027"),
    ("Brazil", "BRA", "#009B3A"),
    ("France", "FRA", "#0055A4"),
    ("Argentina", "ARG", "#5DADEC"),
    ("Spain", "ESP", "#C60B1E"),
    ("Germany", "GER", "#1F1F1F"),
    ("Italy", "ITA", "#008C45"),
    ("Portugal", "POR", "#006600"),
    ("Netherlands", "NED", "#FF6F00"),
    ("England", "ENG", "#B31942"),
    ("Mexico", "MEX", "#006847"),
    ("Korea", "KOR", "#0047A0"),
    ("Morocco", "MAR", "#C1272D"),
    ("Croatia", "CRO", "#171796"),
    ("USA", "USA", "#3C3B6E"),
    ("Australia", "AUS", "#0057B8"),
    ("Senegal", "SEN", "#00853F"),
    ("Uruguay", "URU", "#0038A8"),
    ("Ghana", "GHA", "#FCD116"),
    ("Canada", "CAN", "#D52B1E"),
    ("Colombia", "COL", "#FCD116"),
]


def read_students(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    required = ["学籍番号", "Name", "Kana Name", "English Name", "Department", "Classes Missed"]
    missing = [c for c in required if c not in fieldnames]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    students = []
    for row in rows:
        try:
            missed = int(float(row["Classes Missed"]))
        except Exception:
            missed = 0

        dept = row["Department"].strip()
        is_engineer = (
            "工学部" in dept
            or "工学科" in dept
            or "情報システム" in dept
            or "ロボティクス" in dept
        )

        students.append({
            "id": row["学籍番号"].strip(),
            "name": row["Name"].strip(),
            "kana": row["Kana Name"].strip(),
            "english": row["English Name"].strip(),
            "department": dept,
            "department_label": dept_label(dept),
            "missed": missed,
            "is_engineer": is_engineer,
            "failing_risk": missed >= 5,
        })
    return students


def make_groups(students, group_size=4, seed=None):
    rng = random.Random(seed)

    active = [s for s in students if not s["failing_risk"]]
    failing = [s for s in students if s["failing_risk"]]

    engineers = [s for s in active if s["is_engineer"]]
    non_engineers = [s for s in active if not s["is_engineer"]]

    if not engineers:
        raise ValueError("No active engineers found. Cannot satisfy engineer requirement.")
    if not non_engineers:
        raise ValueError("No active non-engineers found. Cannot prevent engineer-only groups.")

    desired_groups = max(1, math.ceil(len(active) / group_size))
    min_groups_for_engineers = math.ceil(len(engineers) / 2)
    num_groups = min(
        max(desired_groups, min_groups_for_engineers),
        len(engineers),
        len(non_engineers),
    )
    if num_groups < min_groups_for_engineers:
        raise ValueError(
            "Not enough groups available to keep engineers at two per group or fewer."
        )

    groups = [[] for _ in range(num_groups)]
    engineer_counts = [0 for _ in range(num_groups)]

    engineers_sorted = sorted(engineers, key=lambda s: (s["missed"], rng.random()))
    for i, student in enumerate(engineers_sorted[:num_groups]):
        groups[i].append(student)
        engineer_counts[i] = 1

    remaining_engineers = engineers_sorted[num_groups:]
    rng.shuffle(remaining_engineers)
    for student in remaining_engineers:
        candidates = [
            i for i in range(num_groups)
            if engineer_counts[i] < 2
        ]
        if not candidates:
            raise ValueError(
                "Could not spread engineers to no more than two per group."
            )
        target_idx = min(candidates, key=lambda i: (engineer_counts[i], len(groups[i]), rng.random()))
        groups[target_idx].append(student)
        engineer_counts[target_idx] += 1

    rng.shuffle(non_engineers)
    for i in range(num_groups):
        groups[i].append(non_engineers.pop())

    pool = non_engineers
    rng.shuffle(pool)
    for student in pool:
        candidates = [g for g in groups if len(g) < group_size]
        if not candidates:
            candidates = groups
        target = min(candidates, key=lambda g: (len(g), sum(1 for m in g if m["is_engineer"]), rng.random()))
        target.append(student)

    three_member_groups = [
        group for group in groups if sum(1 for m in group if not m["failing_risk"]) == 3
    ]
    rng.shuffle(three_member_groups)
    rng.shuffle(failing)

    for group in three_member_groups:
        for _ in range(2):
            if not failing:
                break
            group.append(failing.pop())

    for student in failing:
        target = min(groups, key=lambda g: (len(g), sum(1 for m in g if m["failing_risk"]), rng.random()))
        target.append(student)

    for group in groups:
        active_members = [s for s in group if not s["failing_risk"]]
        failing_members = [s for s in group if s["failing_risk"]]
        rng.shuffle(active_members)
        rng.shuffle(failing_members)
        group[:] = active_members + failing_members

    countries = COUNTRIES[:]
    rng.shuffle(countries)

    assigned = []
    for i, group in enumerate(groups):
        country, code, color = countries[i % len(countries)]
        assigned.append({
            "group_number": i + 1,
            "country": country,
            "code": code,
            "color": color,
            "members": group,
        })
    return assigned


def write_csv(groups, output_path):
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        fieldnames = [
            "Group",
            "Country",
            "Country Code",
            "学籍番号",
            "Name",
            "Kana Name",
            "English Name",
            "Department",
            "Classes Missed",
            "Affiliation",
            "Failing Risk",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for group in groups:
            for s in group["members"]:
                writer.writerow({
                    "Group": group["group_number"],
                    "Country": group["country"],
                    "Country Code": group["code"],
                    "学籍番号": s["id"],
                    "Name": s["name"],
                    "Kana Name": s["kana"],
                    "English Name": s["english"],
                    "Department": s["department"],
                    "Classes Missed": s["missed"],
                    "Affiliation": "Engineer" if s["is_engineer"] else "Non-engineer",
                    "Failing Risk": "Yes" if s["failing_risk"] else "No",
                })


def dept_label(dept):
    if "工学部" in dept:
        if "ロボティクス" in dept:
            return "Engineering / Robotics"
        return "Engineering"
    if "経済学部" in dept:
        return "Economics"
    if "経営学部" in dept:
        return "Business"
    if "外国語学部" in dept:
        return "Foreign Languages"
    if "国際学部" in dept:
        return "International Studies"
    return "Other"


def write_html(students, output_path, group_size=4):
    students_json = json.dumps(students, ensure_ascii=False)
    countries_json = json.dumps(COUNTRIES, ensure_ascii=False)

    html_text = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Cards and Group Draw</title>
    <style>
        :root {{
            --bg: #ffffff;
            --panel: #ffffff;
            --ink: #111827;
            --muted: #4b5563;
            --line: #d1d5db;
            --soft: #fafafa;
            --risk-bg: #f3f4f6;
            --risk-line: #d1d5db;
            --eng: #0f766e;
            --non: #6d28d9;
            --risk: #6b7280;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background: var(--bg);
            color: var(--ink);
        }}

        body.is-shuffling {{
            overflow: hidden;
        }}

        .app {{
            min-height: 100vh;
        }}

        .topbar {{
            position: sticky;
            top: 0;
            z-index: 20;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(6px);
            border-bottom: none;
            padding: 18px 20px 14px;
        }}

        .topbar-inner {{
            display: flex;
            align-items: stretch;
            justify-content: space-between;
            gap: 24px;
        }}

        .title-block {{
            flex: 1 1 auto;
            align-self: center;
        }}

        .title-block h1 {{
            margin: 0;
            font-size: 17px;
            line-height: 1.1;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .title-block p {{
            margin: 6px 0 0;
            color: var(--muted);
            font-size: 12px;
            line-height: 1.35;
        }}

        .actions {{
            display: flex;
            align-items: stretch;
            gap: 12px;
            flex-wrap: wrap;
            justify-content: flex-end;
            flex: 0 0 auto;
        }}

        .button {{
            appearance: none;
            border: 2px solid #111827;
            background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
            color: white;
            border-radius: 0;
            padding: 18px 28px;
            font-size: 14px;
            font-weight: 900;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            cursor: pointer;
            min-width: 320px;
            min-height: 80px;
            box-shadow: 0 10px 0 #d1d5db;
            transform: translateY(0);
            transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
        }}

        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 0 #d1d5db;
        }}

        .button:active {{
            transform: translateY(6px);
            box-shadow: 0 4px 0 #d1d5db;
        }}

        .button:disabled {{
            opacity: 0.45;
            cursor: default;
            transform: none;
            box-shadow: 0 6px 0 #d1d5db;
        }}

        .button.secondary {{
            min-width: 180px;
            min-height: 54px;
            padding: 12px 18px;
            font-size: 11px;
            letter-spacing: 0.12em;
            background: #ffffff;
            color: #111827;
            border-color: #d1d5db;
            box-shadow: 0 8px 0 #e5e7eb;
        }}

        .button.secondary:hover {{
            box-shadow: 0 10px 0 #e5e7eb;
        }}

        .button.secondary:active {{
            box-shadow: 0 4px 0 #e5e7eb;
        }}

        .summary {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
            padding: 16px 0 4px;
        }}

        .summary-chip {{
            border: none;
            background: #f8fafc;
            border-radius: 0;
            padding: 7px 10px;
            font-size: 11px;
            color: var(--muted);
        }}

        .view {{
            padding: 18px 20px 28px;
        }}

        .section-title {{
            margin: 0 0 14px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: var(--muted);
        }}

        .roster-grid {{
            display: grid;
            gap: 18px;
        }}

        .dept-card {{
            border: none;
            border-radius: 0;
            background: white;
        }}

        .dept-head {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 10px;
            padding: 0 4px 8px;
            border-bottom: none;
            background: transparent;
        }}

        .dept-name {{
            margin: 0;
            font-size: 13px;
            line-height: 1.1;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .dept-count {{
            font-size: 11px;
            color: var(--muted);
        }}

        .student-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 180px));
            justify-content: start;
            gap: 12px;
            padding: 0;
        }}

        .student-card {{
            border: none;
            border-left: 6px solid var(--dept-color, var(--line));
            border-radius: 0;
            padding: 10px 10px 10px 12px;
            background: #fafafa;
            min-height: 78px;
        }}

        .student-card.risk {{
            background: #f4f5f7;
            border-left-color: var(--risk);
            color: #6b7280;
            filter: grayscale(1);
            opacity: 0.92;
        }}

        .student-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }}

        .student-name {{
            font-size: 13px;
            line-height: 1.15;
            font-weight: 800;
        }}

        .student-english {{
            margin-top: 3px;
            font-size: 10px;
            color: var(--muted);
            font-weight: 700;
            letter-spacing: 0.04em;
        }}

        .student-meta {{
            margin-top: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            font-size: 10px;
            color: var(--muted);
        }}

        .tag {{
            flex: 0 0 auto;
            border: 1px solid currentColor;
            border-radius: 0;
            padding: 2px 4px;
            font-size: 9px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            position: relative;
        }}

        .tag.eng {{
            background: #111827;
            border-color: #111827;
            color: white;
        }}

        .tag.non {{
            background: white;
            border-color: #111827;
            color: #111827;
        }}

        .tag.risk {{
            background: #111827;
            border-color: #111827;
            color: white;
        }}

        .tag.risk::after {{
            content: "";
            position: absolute;
            left: 2px;
            right: 2px;
            top: 50%;
            border-top: 1px solid currentColor;
            transform: rotate(-18deg);
            transform-origin: center;
            pointer-events: none;
        }}

        .groups-view {{
            display: none;
            padding: 18px 20px 28px;
        }}

        .groups-view.is-visible {{
            display: block;
        }}

        .groups-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
        }}

        .group-card {{
            border: none;
            border-radius: 0;
            background: white;
        }}

        .group-band {{
            background: var(--team-color);
            color: white;
            padding: 10px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }}

        .group-title {{
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.18em;
        }}

        .group-code {{
            font-size: 16px;
            font-weight: 900;
            letter-spacing: 0.06em;
        }}

        .group-country {{
            margin: 0;
            padding: 10px 4px 8px;
            font-size: 19px;
            line-height: 1;
            text-transform: uppercase;
            color: var(--team-color);
        }}

        .group-members {{
            padding: 0;
            display: grid;
            gap: 10px;
        }}

        .member {{
            border-left: 8px solid var(--team-color);
            border-radius: 0;
            padding: 10px 10px 10px 12px;
            background: white;
        }}

        .member.risk {{
            background: #f4f5f7;
            border-left-color: var(--risk);
            color: #6b7280;
        }}

        .member-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }}

        .name {{
            font-size: 14px;
            line-height: 1.15;
            font-weight: 800;
        }}

        .english {{
            margin-top: 3px;
            font-size: 10px;
            color: var(--muted);
            font-weight: 700;
            letter-spacing: 0.04em;
        }}

        .dept {{
            margin-top: 4px;
            font-size: 11px;
            line-height: 1.2;
        }}

        .missed {{
            margin-top: 3px;
            font-size: 10px;
            color: var(--muted);
        }}

        .badge {{
            flex: 0 0 auto;
            border: none;
            border-radius: 0;
            color: white;
            font-size: 9px;
            font-weight: 900;
            padding: 4px 6px;
            letter-spacing: 0.05em;
            position: relative;
        }}

        .badge.eng {{
            background: #111827;
            border-color: #111827;
            color: white;
        }}

        .badge.non {{
            background: white;
            border: 1px solid #111827;
            color: #111827;
        }}

        .member.risk .badge {{
            background: #111827;
            border-color: #111827;
            color: white;
        }}

        .badge.risk::after {{
            content: "";
            position: absolute;
            left: 3px;
            right: 3px;
            top: 50%;
            border-top: 1px solid rgba(255,255,255,0.95);
            transform: rotate(-18deg);
            transform-origin: center;
            pointer-events: none;
        }}

        .shuffle-overlay {{
            position: fixed;
            inset: 0;
            z-index: 50;
            background: white;
            display: none;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            padding: 24px;
        }}

        .shuffle-overlay.is-visible {{
            display: flex;
        }}

        .shuffle-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.22em;
            color: var(--muted);
            margin-bottom: 10px;
        }}

        .shuffle-line {{
            font-size: clamp(22px, 4vw, 46px);
            line-height: 1.1;
            font-weight: 800;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            padding: 0 12px;
            max-width: 100%;
        }}

        .shuffle-sub {{
            margin-top: 10px;
            font-size: 12px;
            color: var(--muted);
        }}

        body.is-shuffling .topbar,
        body.is-shuffling .view {{
            visibility: hidden;
        }}

        body.is-shuffling .shuffle-overlay {{
            visibility: visible;
        }}

        .legend {{
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            padding: 10px 20px 6px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 7px;
            border-radius: 0;
            padding: 4px 0;
            font-size: 11px;
            color: var(--muted);
            background: transparent;
        }}

        .legend-label {{
            font-weight: 700;
        }}

        .legend-mark {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 14px;
            height: 14px;
            flex: 0 0 auto;
        }}

        .legend-item.eng {{
            color: #111827;
        }}

        .legend-item.non {{
            color: #111827;
        }}

        .legend-item.risk {{
            color: #6b7280;
        }}

        .legend-item.eng .legend-mark {{
            background: #111827;
        }}

        .legend-item.non .legend-mark {{
            border: 1.5px solid #111827;
            background: transparent;
        }}

        .legend-item.risk .legend-mark {{
            position: relative;
            border: 1px solid #9ca3af;
            background: transparent;
        }}

        .legend-item.risk .legend-mark::after {{
            content: "";
            width: 8px;
            height: 2px;
            background: #9ca3af;
            transform: rotate(-20deg);
            position: absolute;
        }}

        @media (max-width: 760px) {{
            .student-list {{
                grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            }}
        }}

        header {{
            padding: 18px 20px 12px;
            text-align: center;
        }}

        header .kicker {{
            color: var(--muted);
            letter-spacing: 0.18em;
            text-transform: uppercase;
            font-size: 11px;
            font-weight: 700;
        }}

        header h1 {{
            margin: 6px 0 6px;
            font-size: clamp(22px, 3vw, 38px);
            line-height: 1;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        header p {{
            margin: 0 auto;
            max-width: 720px;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.4;
        }}

        footer {{
            text-align: center;
            padding: 0 20px 18px;
            color: var(--muted);
            font-size: 11px;
        }}

        @media print {{
            body {{ background: white; }}
            header, footer {{ color: black; }}
            header p {{ color: #333; }}
            main {{ width: 100%; grid-template-columns: repeat(3, 1fr); gap: 6px; }}
            .group-card {{ box-shadow: none; break-inside: avoid; }}
        }}
    </style>
</head>

<body>
    <div class="app">
        <div class="topbar">
            <div class="topbar-inner">
                <div class="title-block">
                    <h1>Student Cards and Group Draw</h1>
                    <p>Students are shown by department first. Press create groups to shuffle the names, then reveal balanced groups.</p>
                </div>
                <div class="actions">
                    <button id="create-groups" class="button" type="button">Create Groups</button>
                    <button id="download-csv" class="button secondary" type="button" disabled>Download CSV</button>
                </div>
            </div>
            <div id="summary" class="summary"></div>
        </div>

        <div class="legend">
            <div class="legend-item eng"><span class="legend-mark"></span><span class="legend-label">Engineering</span></div>
            <div class="legend-item non"><span class="legend-mark"></span><span class="legend-label">Non-engineering</span></div>
            <div class="legend-item risk"><span class="legend-mark"></span><span class="legend-label">5+ absences</span></div>
        </div>

        <section id="roster-view" class="view">
            <h2 class="section-title">Students by Department</h2>
            <div id="roster-grid" class="roster-grid"></div>
        </section>

        <section id="groups-view" class="groups-view">
            <h2 class="section-title">Groups</h2>
            <div id="groups-grid" class="groups-grid"></div>
        </section>
    </div>

    <div id="shuffle-overlay" class="shuffle-overlay" aria-hidden="true">
        <div class="shuffle-label">Creating groups</div>
        <div id="shuffle-line" class="shuffle-line">Shuffling names...</div>
        <div class="shuffle-sub">Rapid fire draw in progress</div>
    </div>

    <script>
        const STUDENTS = __STUDENTS_JSON__;
        const COUNTRIES = __COUNTRIES_JSON__;
        const GROUP_SIZE = __GROUP_SIZE__;

        const DEPT_COLORS = {{
            "Engineering": "#0f766e",
            "Engineering / Robotics": "#0f766e",
            "Economics": "#6d28d9",
            "Business": "#b45309",
            "Foreign Languages": "#0369a1",
            "International Studies": "#be185d",
            "Other": "#475569"
        }};

        const DEPT_ORDER = [
            "Engineering",
            "Engineering / Robotics",
            "Economics",
            "Business",
            "Foreign Languages",
            "International Studies",
            "Other"
        ];

        const rosterGrid = document.getElementById("roster-grid");
        const groupsGrid = document.getElementById("groups-grid");
        const summary = document.getElementById("summary");
        const createButton = document.getElementById("create-groups");
        const downloadButton = document.getElementById("download-csv");
        const rosterView = document.getElementById("roster-view");
        const groupsView = document.getElementById("groups-view");
        const overlay = document.getElementById("shuffle-overlay");
        const shuffleLine = document.getElementById("shuffle-line");
        let lastGroups = null;

        function shuffle(array) {{
            const copy = array.slice();
            for (let i = copy.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [copy[i], copy[j]] = [copy[j], copy[i]];
            }}
            return copy;
        }}

        function colorForDept(label) {{
            return DEPT_COLORS[label] || DEPT_COLORS.Other;
        }}

        function deptBuckets(students) {{
            const buckets = new Map();
            for (const student of students) {{
                const label = student.department_label || "Other";
                if (!buckets.has(label)) {{
                    buckets.set(label, []);
                }}
                buckets.get(label).push(student);
            }}
            return buckets;
        }}

        function renderSummary() {{
            const engineers = STUDENTS.filter((s) => s.is_engineer).length;
            const nonEngineers = STUDENTS.filter((s) => !s.is_engineer).length;
            const risk = STUDENTS.filter((s) => s.failing_risk).length;
            summary.innerHTML = [
                `<div class="summary-chip">Students: ${STUDENTS.length}</div>`,
                `<div class="summary-chip">Engineers: ${engineers}</div>`,
                `<div class="summary-chip">Non-engineers: ${nonEngineers}</div>`,
                `<div class="summary-chip">5+ absences: ${risk}</div>`
            ].join("");
        }}

        function renderRoster() {{
            const buckets = deptBuckets(STUDENTS);
            const ordered = Array.from(buckets.keys()).sort((a, b) => {{
                const ia = DEPT_ORDER.indexOf(a);
                const ib = DEPT_ORDER.indexOf(b);
                if (ia === -1 && ib === -1) return a.localeCompare(b);
                if (ia === -1) return 1;
                if (ib === -1) return -1;
                return ia - ib;
            }});

            rosterGrid.innerHTML = ordered.map((dept) => {{
                const students = buckets.get(dept).slice().sort((a, b) => {{
                    if (a.failing_risk !== b.failing_risk) return Number(a.failing_risk) - Number(b.failing_risk);
                    return (a.english || a.name).localeCompare(b.english || b.name);
                }});

                return `
                    <article class="dept-card" style="--dept-color: ${colorForDept(dept)}">
                        <div class="dept-head">
                            <h3 class="dept-name">${dept}</h3>
                            <div class="dept-count">${students.length} students</div>
                        </div>
                        <div class="student-list">
                            ${students.map((s) => `
                            <div class="student-card${s.failing_risk ? " risk" : ""}">
                                <div class="student-top">
                                    <div class="student-name">${escapeHtml(s.name)}</div>
                                    <div class="tag ${s.is_engineer ? "eng" : "non"}${s.failing_risk ? " risk" : ""}">${s.is_engineer ? "ENG" : "NON"}</div>
                                </div>
                                <div class="student-english">${escapeHtml(s.english)}</div>
                                <div class="student-meta">
                                    <span>Missed: ${s.missed}</span>
                                </div>
                            </div>
                        `).join("")}
                    </div>
                </article>
                `;
            }}).join("");
        }}

        function escapeHtml(value) {{
            return String(value)
                .replaceAll("&", "&amp;")
                .replaceAll("<", "&lt;")
                .replaceAll(">", "&gt;")
                .replaceAll('"', "&quot;")
                .replaceAll("'", "&#39;");
        }}

        function randomByMissed(items) {{
            return items
                .map((item) => ({{ item, noise: Math.random() }}))
                .sort((a, b) => (a.item.missed - b.item.missed) || (a.noise - b.noise))
                .map((entry) => entry.item);
        }}

        function makeGroups(students, groupSize) {{
            const active = students.filter((s) => !s.failing_risk);
            const failing = students.filter((s) => s.failing_risk);
            const engineers = active.filter((s) => s.is_engineer);
            const nonEngineers = active.filter((s) => !s.is_engineer);

            if (!engineers.length) {{
                throw new Error("No active engineers found.");
            }}
            if (!nonEngineers.length) {{
                throw new Error("No active non-engineers found.");
            }}

            const desiredGroups = Math.max(1, Math.ceil(active.length / groupSize));
            const minGroupsForEngineers = Math.ceil(engineers.length / 2);
            const numGroups = Math.min(
                Math.max(desiredGroups, minGroupsForEngineers),
                engineers.length,
                nonEngineers.length
            );

            if (numGroups < minGroupsForEngineers) {{
                throw new Error("Not enough groups available to keep engineers at two per group or fewer.");
            }}

            const groups = Array.from({{ length: numGroups }}, () => ({{ members: [], engineerCount: 0 }}));
            const engineersSorted = randomByMissed(engineers);

            engineersSorted.slice(0, numGroups).forEach((student, index) => {{
                groups[index].members.push(student);
                groups[index].engineerCount = 1;
            }});

            const remainingEngineers = shuffle(engineersSorted.slice(numGroups));
            remainingEngineers.forEach((student) => {{
                const candidates = groups
                    .map((group, index) => ({{ group, index }}))
                    .filter((entry) => entry.group.engineerCount < 2);

                if (!candidates.length) {{
                    throw new Error("Could not spread engineers to no more than two per group.");
                }}

                candidates.sort((a, b) => (
                    a.group.engineerCount - b.group.engineerCount ||
                    a.group.members.length - b.group.members.length ||
                    Math.random() - 0.5
                ));

                candidates[0].group.members.push(student);
                candidates[0].group.engineerCount += 1;
            }});

            const nonEngineerPool = shuffle(nonEngineers);
            for (let i = 0; i < groups.length; i++) {{
                groups[i].members.push(nonEngineerPool.pop());
            }}

            shuffle(nonEngineerPool).forEach((student) => {{
                const candidates = groups.filter((group) => group.members.length < groupSize);
                const targetPool = candidates.length ? candidates : groups;
                targetPool.sort((a, b) => (
                    a.members.length - b.members.length ||
                    a.members.filter((member) => member.is_engineer).length - b.members.filter((member) => member.is_engineer).length ||
                    Math.random() - 0.5
                ));
                targetPool[0].members.push(student);
            }});

            const threeMemberGroups = groups.filter((group) => (
                group.members.filter((member) => !member.failing_risk).length === 3
            ));
            shuffle(threeMemberGroups);
            const failingPool = shuffle(failing);

            threeMemberGroups.forEach((group) => {{
                for (let i = 0; i < 2 && failingPool.length > 0; i++) {{
                    group.members.push(failingPool.shift());
                }}
            }});

            failingPool.forEach((student) => {{
                groups.sort((a, b) => (
                    a.members.length - b.members.length ||
                    a.members.filter((member) => member.failing_risk).length - b.members.filter((member) => member.failing_risk).length ||
                    Math.random() - 0.5
                ));
                groups[0].members.push(student);
            }});

            const countries = shuffle(COUNTRIES).slice();
            return groups.map((group, index) => {{
                const country = countries[index % countries.length];
                const activeMembers = group.members.filter((member) => !member.failing_risk);
                const failingMembers = group.members.filter((member) => member.failing_risk);
                return {{
                    groupNumber: index + 1,
                    country: country[0],
                    code: country[1],
                    color: country[2],
                    members: shuffle(activeMembers).concat(shuffle(failingMembers))
                }};
            }});
        }}

        function renderGroups(groups) {{
            groupsGrid.innerHTML = groups.map((group) => `
                <article class="group-card" style="--team-color: ${group.color}">
                    <div class="group-band">
                        <div class="group-title">GROUP ${String(group.groupNumber).padStart(2, "0")}</div>
                        <div class="group-code">${group.code}</div>
                    </div>
                    <h3 class="group-country">${group.country}</h3>
                    <div class="group-members">
                        ${group.members.map((student) => `
                            <div class="member${student.failing_risk ? " risk" : ""}">
                                <div class="member-top">
                                    <div class="name">${escapeHtml(student.name)}</div>
                                    <div class="badge ${student.is_engineer ? "eng" : "non"}${student.failing_risk ? " risk" : ""}">${student.is_engineer ? "ENG" : "NON"}</div>
                                </div>
                                <div class="english">${escapeHtml(student.english)}</div>
                                <div class="dept">${escapeHtml(student.department_label)}</div>
                                <div class="missed">Missed: ${student.missed}</div>
                            </div>
                        `).join("")}
                    </div>
                </article>
            `).join("");
        }}

        function csvCell(value) {{
            const text = String(value ?? "");
            if (/[",\\n\\r]/.test(text)) {{
                return `"${text.replaceAll('"', '""')}"`;
            }}
            return text;
        }}

        function buildCsv(groups) {{
            const header = [
                "Group",
                "Country",
                "Country Code",
                "学籍番号",
                "Name",
                "Kana Name",
                "English Name",
                "Department",
                "Classes Missed",
                "Affiliation",
                "Failing Risk"
            ];

            const rows = [header.join(",")];
            groups.forEach((group) => {{
                group.members.forEach((student) => {{
                    rows.push([
                        group.groupNumber,
                        group.country,
                        group.code,
                        student.id,
                        student.name,
                        student.kana,
                        student.english,
                        student.department,
                        student.missed,
                        student.is_engineer ? "Engineer" : "Non-engineer",
                        student.failing_risk ? "Yes" : "No"
                    ].map(csvCell).join(","));
                }});
            }});
            return rows.join("\\r\\n");
        }}

        function downloadCsv(groups) {{
            const csv = buildCsv(groups);
            const blob = new Blob([String.fromCharCode(0xfeff), csv], {{ type: "text/csv;charset=utf-8" }});
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = "groups_output.csv";
            document.body.appendChild(link);
            link.click();
            link.remove();
            setTimeout(() => URL.revokeObjectURL(url), 2000);
        }}

        function sleep(ms) {{
            return new Promise((resolve) => setTimeout(resolve, ms));
        }}

        async function createGroups() {{
            createButton.disabled = true;
            document.body.classList.add("is-shuffling");
            overlay.classList.add("is-visible");

            const pool = STUDENTS.map((student) => student.english || student.name);
            const lineParts = [];
            const ticker = setInterval(() => {{
                lineParts.push(pool[Math.floor(Math.random() * pool.length)]);
                if (lineParts.length > 6) {{
                    lineParts.shift();
                }}
                shuffleLine.textContent = lineParts.join("   •   ");
            }}, 55);

            await sleep(3200);
            clearInterval(ticker);

            lastGroups = makeGroups(STUDENTS, GROUP_SIZE);
            renderGroups(lastGroups);
            rosterView.style.display = "none";
            groupsView.classList.add("is-visible");
            downloadButton.disabled = false;

            overlay.classList.remove("is-visible");
            document.body.classList.remove("is-shuffling");
            createButton.textContent = "Groups Created";
        }}

        renderSummary();
        renderRoster();
        createButton.addEventListener("click", createGroups);
        downloadButton.addEventListener("click", () => {{
            if (lastGroups) {{
                downloadCsv(lastGroups);
            }}
        }});
    </script>

    <footer>
        Generated by create_groups_worldcup.py. Use the Download CSV button to save groups_output.csv.
    </footer>
</body>

</html>
""".replace("__STUDENTS_JSON__", students_json).replace("__COUNTRIES_JSON__", countries_json).replace("__GROUP_SIZE__", str(group_size)).replace("{{", "{").replace("}}", "}")
    Path(output_path).write_text(html_text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="merged_roster_attendance.csv")
    parser.add_argument("--group-size", type=int, default=4)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--csv-output", default="groups_output.csv")
    parser.add_argument("--html-output", default="groups_worldcup.html")
    args = parser.parse_args()

    students = read_students(args.input)
    groups = make_groups(students, group_size=args.group_size, seed=args.seed)

    write_csv(groups, args.csv_output)
    write_html(students, args.html_output, group_size=args.group_size)

    active_count = sum(1 for s in students if not s["failing_risk"])
    risk_count = sum(1 for s in students if s["failing_risk"])

    print("Group creation complete.")
    print(f"Active students grouped first: {active_count}")
    print(f"Students with 5+ absences added after: {risk_count}")
    print(f"Groups created: {len(groups)}")
    print(f"CSV output: {args.csv_output}")
    print(f"HTML output: {args.html_output}")


if __name__ == "__main__":
    main()
