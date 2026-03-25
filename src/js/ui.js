const FLAGS= {
    //ASIA
    AFG: "🇦🇫", ARM: "🇦🇲", AZE: "🇦🇿", BHR: "🇧🇭", BGD: "🇧🇩",
    BTN: "🇧🇹", BRN: "🇧🇳", KHM: "🇰🇭", CHN: "🇨🇳", CYP: "🇨🇾",
    GEO: "🇬🇪", IND: "🇮🇳", IDN: "🇮🇩", IRN: "🇮🇷", IRQ: "🇮🇶",
    ISR: "🇮🇱", JPN: "🇯🇵", JOR: "🇯🇴", KAZ: "🇰🇿", KWT: "🇰🇼",
    KGZ: "🇰🇬", LAO: "🇱🇦", LBN: "🇱🇧", MAC: "🇲🇴", MYS: "🇲🇾",
    MDV: "🇲🇻", MNG: "🇲🇳", MMR: "🇲🇲", NPL: "🇳🇵", PRK: "🇰🇵",
    OMN: "🇴🇲", PAK: "🇵🇰", PSE: "🇵🇸", PHL: "🇵🇭", QAT: "🇶🇦",
    SAU: "🇸🇦", KSA: "🇸🇦", SGP: "🇸🇬", KOR: "🇰🇷", LKA: "🇱🇰",
    SYR: "🇸🇾", TWN: "🇹🇼", TJK: "🇹🇯", THA: "🇹🇭", TLS: "🇹🇱",
    TKM: "🇹🇲", UAE: "🇦🇪", UZB: "🇺🇿", VNM: "🇻🇳", YEM: "🇾🇪",
    //EUROPE
    ALB: "🇦🇱", AND: "🇦🇩", AUT: "🇦🇹", BLR: "🇧🇾", BEL: "🇧🇪",
    BIH: "🇧🇦", BGR: "🇧🇬", HRV: "🇭🇷", CZE: "🇨🇿", DNK: "🇩🇰",
    EST: "🇪🇪", FIN: "🇫🇮", FRA: "🇫🇷", DEU: "🇩🇪", GRC: "🇬🇷",
    HUN: "🇭🇺", ISL: "🇮🇸", IRL: "🇮🇪", ITA: "🇮🇹", LVA: "🇱🇻",
    LIE: "🇱🇮", LTU: "🇱🇹", LUX: "🇱🇺", MLT: "🇲🇹", MDA: "🇲🇩",
    MCO: "🇲🇨", MNE: "🇲🇪", NLD: "🇳🇱", MKD: "🇲🇰", NOR: "🇳🇴",
    POL: "🇵🇱", PRT: "🇵🇹", ROU: "🇷🇴", RUS: "🇷🇺", SMR: "🇸🇲",
    SRB: "🇷🇸", SVK: "🇸🇰", SVN: "🇸🇮", ESP: "🇪🇸", SWE: "🇸🇪",
    CHE: "🇨🇭", TUR: "🇹🇷", UKR: "🇺🇦", GBR: "🇬🇧", ENG: "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    SCO: "🏴󠁧󠁢󠁳󠁣󠁴󠁿", WAL: "🏴󠁧󠁢󠁷󠁬󠁳󠁿", VAT: "🇻🇦", KOS: "🇽🇰",
    //AFRICA
    DZA: "🇩🇿", AGO: "🇦🇴", BEN: "🇧🇯", BWA: "🇧🇼", BFA: "🇧🇫",
    BDI: "🇧🇮", CPV: "🇨🇻", CMR: "🇨🇲", CAF: "🇨🇫", TCD: "🇹🇩",
    COM: "🇰🇲", COD: "🇨🇩", COG: "🇨🇬", CIV: "🇨🇮", DJI: "🇩🇯",
    EGY: "🇪🇬", GNQ: "🇬🇶", ERI: "🇪🇷", SWZ: "🇸🇿", ETH: "🇪🇹",
    GAB: "🇬🇦", GMB: "🇬🇲", GHA: "🇬🇭", GIN: "🇬🇳", GNB: "🇬🇼",
    KEN: "🇰🇪", LSO: "🇱🇸", LBR: "🇱🇷", LBY: "🇱🇾", MDG: "🇲🇬",
    MWI: "🇲🇼", MLI: "🇲🇱", MRT: "🇲🇷", MUS: "🇲🇺", MAR: "🇲🇦",
    MOZ: "🇲🇿", NAM: "🇳🇦", NER: "🇳🇪", NGA: "🇳🇬", RWA: "🇷🇼",
    STP: "🇸🇹", SEN: "🇸🇳", SLE: "🇸🇱", SOM: "🇸🇴", ZAF: "🇿🇦",
    SSD: "🇸🇸", SDN: "🇸🇩", TZA: "🇹🇿", TGO: "🇹🇬", TUN: "🇹🇳",
    UGA: "🇺🇬", ZMB: "🇿🇲", ZWE: "🇿🇼",
    //AMERICAS
    ARG: "🇦🇷", BOL: "🇧🇴", BRA: "🇧🇷", CAN: "🇨🇦", CHL: "🇨🇱",
    COL: "🇨🇴", CRI: "🇨🇷", CUB: "🇨🇺", DOM: "🇩🇴", ECU: "🇪🇨",
    SLV: "🇸🇻", GUA: "🇬🇹", HTI: "🇭🇹", HND: "🇭🇳", JAM: "🇯🇲",
    MEX: "🇲🇽", NCA: "🇳🇮", PAN: "🇵🇦", PRY: "🇵🇾", PER: "🇵🇪",
    PRI: "🇵🇷", TTO: "🇹🇹", USA: "🇺🇸", URY: "🇺🇾", VEN: "🇻🇪",
    //OCEANIA
    AUS: "🇦🇺", FIJ: "🇫🇯", NZL: "🇳🇿", PNG: "🇵🇬", WSM: "🇼🇸",
    SOL: "🇸🇧", VUT: "🇻🇺", TON: "🇹🇴",
};

const ui= {
    flag(code) {
        return FLAGS[code] || "🏳️";
    },

    badge(status) {
        const map= {
            played:    ["badge_played",    "Played"],
            scheduled: ["badge_scheduled", "Scheduled"],
            live:      ["badge_live",      "Live"],
            postponed: ["badge_postponed", "Postponed"],
        };
        const [cls, label]= map[status] || ["badge_default", status || "Unknown"];
        return `<span class="badge ${cls}">${label}</span>`;
    },

    formatDate(str) {
        if (!str) return "—";
        return new Date(str).toLocaleDateString("en-GB", {day: "numeric", month: "short", year: "numeric"});
    },

    formatTime(str) {
        if (!str || str === "00:00:00") return "";
        return str.slice(0, 5) + " UTC";
    },

    matchCard(m) {
        const homeAbbr= m.home_team_abbr || "TBD";
        const awayAbbr= m.away_team_abbr || "TBD";
        const centre= m.status === "played"
            ? `<div class="match_card_score"><div class="match_card_score_num">${m.home_goals ?? 0} – ${m.away_goals ?? 0}</div></div>`
            : `<div class="match_card_vs">${ui.formatTime(m.time_venue_utc) || "VS"}</div>`;

        return `
        <article class="match_card" data-id="${m.id}">
            <div class="match_card_header">
                <span class="match_card_competition">${m.competition_name || ""}</span>
                <span class="match_card_stage">${m.stage_name || ""}</span>
            </div>
            <div class="match_card_teams">
                <div class="match_card_team match_card_team_home">
                    <div class="match_card_flag">${ui.flag(m.home_team_country)}</div>
                    <div class="match_card_abbr">${homeAbbr}</div>
                    <div class="match_card_name">${m.home_team_name || "TBD"}</div>
                </div>
                ${centre}
                <div class="match_card_team match_card_team_away">
                    <div class="match_card_flag">${ui.flag(m.away_team_country)}</div>
                    <div class="match_card_abbr">${awayAbbr}</div>
                    <div class="match_card_name">${m.away_team_name || "TBD"}</div>
                </div>
            </div>
            <div class="match_card_footer">
                <div class="match_card_date">
                    ${ui.formatDate(m.date_venue)}
                    ${m.time_venue_utc && m.time_venue_utc !== "00:00:00" ? "· " + ui.formatTime(m.time_venue_utc) : ""}
                </div>
                ${ui.badge(m.status)}
            </div>
        </article>`;
    },

    renderGrid(matches, container) {
        if (!matches.length) {
            container.innerHTML= `<div class="empty_state"><p>No matches found.</p></div>`;
            return;
        }
        container.innerHTML= matches
            .map((m, i) => ui.matchCard(m).replace('class="match_card"', `class="match_card" style="animation-delay:${i * 0.05}s"`))
            .join("");
    },

    renderDetail(m) {
        const winner= m.winner_name ? `<div class="detail_winner">Winner: ${m.winner_name}</div>` : "";
        return `
        <div class="detail_comp">${m.competition_name || ""}</div>
        <div class="detail_meta">
            ${m.stage_name || ""} · Season ${m.season || ""}
            · ${ui.formatDate(m.date_venue)}
            ${m.time_venue_utc && m.time_venue_utc !== "00:00:00" ? "at " + ui.formatTime(m.time_venue_utc) : ""}
            ${m.stadium ? "· " + m.stadium : ""}
        </div>
        <div class="detail_scoreboard">
            <div class="detail_team detail_team_home">
                <div class="detail_team_abbr">${m.home_team_abbr || "TBD"}</div>
                <div class="detail_team_name">${m.home_team_name || "TBD"}</div>
                <div class="detail_team_country">${ui.flag(m.home_team_country)} ${m.home_team_country || ""}</div>
            </div>
            <div>
                <div class="detail_score">${m.home_goals ?? "–"} – ${m.away_goals ?? "–"}</div>
                <div style="text-align:center;margin-top:8px">${ui.badge(m.status)}</div>
            </div>
            <div class="detail_team detail_team_away">
                <div class="detail_team_abbr">${m.away_team_abbr || "TBD"}</div>
                <div class="detail_team_name">${m.away_team_name || "TBD"}</div>
                <div class="detail_team_country">${ui.flag(m.away_team_country)} ${m.away_team_country || ""}</div>
            </div>
        </div>
        ${winner}
        ${m.events && m.events.length ? `
            <div style="margin-top:16px">
                <p style="font-size:13px;font-weight:700;text-transform:uppercase;color:var(--text_muted);margin-bottom:8px">Events</p>
                ${m.events.map(e => `
                    <div style="display:flex;gap:12px;font-size:13px;padding:8px 12px;background:var(--off_white);border-radius:var(--radius);margin-bottom:6px">
                        <span style="color:var(--blue);font-weight:700;min-width:32px">${e.minute ? e.minute + "'" : "—"}</span>
                        <span style="color:var(--text_muted)">${e.event_type}</span>
                        <span>${e.team_name || ""}</span>
                    </div>`).join("")}
            </div>` : ""}`;
    },

    showToast(msg, isError= false) {
        const el= document.getElementById("toast");
        el.textContent= msg;
        el.className= "toast show" + (isError ? " error" : "");
        setTimeout(() => { el.className= "toast"; }, 3200);
    },

    openModal(id) {
        document.getElementById(id).classList.add("is_open");
        document.body.style.overflow= "hidden";
    },

    closeModal(id) {
        document.getElementById(id).classList.remove("is_open");
        document.body.style.overflow= "";
    },
};