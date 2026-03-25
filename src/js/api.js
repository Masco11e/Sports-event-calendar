const api= {
    async getMatches(filters= {}) {
        const params= new URLSearchParams();
        if (filters.competition) params.set("competition", filters.competition);
        if (filters.status)      params.set("status",      filters.status);
        if (filters.date_from)   params.set("date_from",   filters.date_from);
        if (filters.date_to)     params.set("date_to",     filters.date_to);
        const res= await fetch(`/api/matches?${params}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    },

    async getMatch(id) {
        const res= await fetch(`/api/matches/${id}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    },

    async createMatch(data) {
        const res= await fetch("/api/matches", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data),
        });
        const json= await res.json();
        if (!res.ok) throw new Error(json.error || `HTTP ${res.status}`);
        return json;
    },

    async getCompetitions() {
        const res= await fetch("/api/competitions");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    },
};