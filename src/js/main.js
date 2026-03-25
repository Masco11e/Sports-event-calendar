(async function init() {
    const grid=           document.getElementById("matchGrid");
    const filterComp=     document.getElementById("filterCompetition");
    const filterStatus=   document.getElementById("filterStatus");
    const filterDateFrom= document.getElementById("filterDateFrom");
    const filterDateTo=   document.getElementById("filterDateTo");

    try {
        const comps= await api.getCompetitions();
        comps.forEach(c => {
            const opt= document.createElement("option");
            opt.value= c.id;
            opt.textContent= c.name;
            filterComp.appendChild(opt);
        });
    } catch (_) {}

    async function loadMatches() {
        grid.innerHTML= `<div class="loading_state"><div class="spinner"></div><p>Loading matches…</p></div>`;
        try {
            const matches= await api.getMatches({
                competition: filterComp.value,
                status:      filterStatus.value,
                date_from:   filterDateFrom.value,
                date_to:     filterDateTo.value,
            });
            ui.renderGrid(matches, grid);
        } catch (err) {
            grid.innerHTML= `<div class="empty_state"><p>Failed to load matches.</p></div>`;
            console.error(err);
        }
    }

    document.getElementById("applyFilters").addEventListener("click", loadMatches);
    document.getElementById("clearFilters").addEventListener("click", () => {
        filterComp.value=     "";
        filterStatus.value=   "";
        filterDateFrom.value= "";
        filterDateTo.value=   "";
        loadMatches();
    });

    grid.addEventListener("click", async (e) => {
        const card= e.target.closest(".match_card");
        if (!card) return;
        try {
            const match= await api.getMatch(card.dataset.id);
            document.getElementById("detailContent").innerHTML= ui.renderDetail(match);
            ui.openModal("detailModal");
        } catch (err) {
            ui.showToast("Could not load match details.", true);
        }
    });

    document.getElementById("closeDetailModal").addEventListener("click", () => ui.closeModal("detailModal"));
    document.getElementById("detailModal").addEventListener("click", (e) => {
        if (e.target === e.currentTarget) ui.closeModal("detailModal");
    });

    document.getElementById("openAddModal").addEventListener("click", () => {
        const today= new Date();
        const dateStr= today.toISOString().split("T")[0];
        document.querySelector("[name='date_venue']").value= dateStr;
        document.querySelector("[name='season']").value= today.getFullYear();
        ui.openModal("addModal");
    });

    const closeAdd= () => {
        ui.closeModal("addModal");
        document.getElementById("addForm").reset();
        document.getElementById("formError").classList.add("hidden");
    };

    document.getElementById("closeAddModal").addEventListener("click", closeAdd);
    document.getElementById("cancelAdd").addEventListener("click", closeAdd);
    document.getElementById("addModal").addEventListener("click", (e) => {
        if (e.target === e.currentTarget) closeAdd();
    });

    document.getElementById("addForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const btn=   e.target.querySelector(".btn_submit");
        const errEl= document.getElementById("formError");
        const fd=    new FormData(e.target);
        const get=   k => fd.get(k)?.trim() || null;

        const buildTeam= prefix => {
            const slug= get(`${prefix}_slug`);
            if (!slug) return null;
            return {
                slug,
                name:          get(`${prefix}_name`) || slug,
                official_name: get(`${prefix}_name`) || slug,
                abbreviation:  get(`${prefix}_abbr`) || slug.slice(0, 3).toUpperCase(),
                country_code:  get(`${prefix}_country`) || "",
            };
        };

        const body= {
            competition_name: get("competition_name"),
            _stage_id:        get("_stage_id"),
            stage_name:       get("_stage_id"),
            season:           parseInt(get("season"), 10),
            date_venue:       get("date_venue"),
            time_venue_utc:   get("time_venue_utc") ? get("time_venue_utc") + ":00" : "00:00:00",
            status:           get("status"),
            stadium:          get("stadium"),
            home_team:        buildTeam("home"),
            away_team:        buildTeam("away"),
        };

        btn.disabled=    true;
        btn.textContent= "Saving…";
        errEl.classList.add("hidden");

        try {
            await api.createMatch(body);
            closeAdd();
            ui.showToast("Match added successfully!");
            await loadMatches();
        } catch (err) {
            errEl.textContent= err.message;
            errEl.classList.remove("hidden");
        } finally {
            btn.disabled=    false;
            btn.textContent= "Create Match";
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") { ui.closeModal("detailModal"); closeAdd(); }
    });

    loadMatches();
})();