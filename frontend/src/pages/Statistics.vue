<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../services/api";
import { spaceName } from "../services/space";
import {
    BarChart3,
    ClipboardList,
    CircleCheck,
    TriangleAlert,
    Star,
} from "lucide-vue-next";

import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    PointElement,
    LineElement,
    Filler,
} from "chart.js";

import { Doughnut, Bar, Line } from "vue-chartjs";

ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    PointElement,
    LineElement,
    Filler
);

const tasks = ref([]);
const loading = ref(true);

const loadTasks = async () => {
    try {
        const response = await api.get("tasks/");
        tasks.value = response.data;
    } catch (error) {
        console.error(error);
    } finally {
        loading.value = false;
    }
};

// ===============================
// COMPTEURS
// ===============================

const total = computed(() => tasks.value.length);
const done = computed(
    () => tasks.value.filter((t) => t.status === "done").length
);
const overdue = computed(
    () => tasks.value.filter((t) => t.is_overdue).length
);
const favorites = computed(
    () => tasks.value.filter((t) => t.is_favorite).length
);

const progress = computed(() =>
    total.value === 0 ? 0 : Math.round((done.value / total.value) * 100)
);

// ===============================
// DOUGHNUT : STATUTS
// ===============================

const statusData = computed(() => ({
    labels: ["À faire", "En cours", "À vérifier", "Terminées"],
    datasets: [
        {
            data: [
                tasks.value.filter((t) => t.status === "todo").length,
                tasks.value.filter((t) => t.status === "in_progress")
                    .length,
                tasks.value.filter((t) => t.status === "review").length,
                done.value,
            ],
            backgroundColor: ["#3b82f6", "#f59e0b", "#8b5cf6", "#22c55e"],
            borderColor: "transparent",
            hoverOffset: 6,
        },
    ],
}));

const doughnutOptions = {
    cutout: "68%",
    plugins: {
        legend: {
            position: "bottom",
            labels: {
                color: "#94a3b8",
                padding: 16,
                usePointStyle: true,
                pointStyle: "circle",
            },
        },
    },
};

// ===============================
// BAR : PRIORITÉS
// ===============================

const priorityData = computed(() => ({
    labels: ["Faible", "Moyenne", "Élevée", "Urgente"],
    datasets: [
        {
            label: "Tâches",
            data: [
                tasks.value.filter((t) => t.priority === "low").length,
                tasks.value.filter((t) => t.priority === "medium")
                    .length,
                tasks.value.filter((t) => t.priority === "high").length,
                tasks.value.filter((t) => t.priority === "urgent")
                    .length,
            ],
            backgroundColor: ["#22c55e", "#f59e0b", "#ef4444", "#dc2626"],
            borderRadius: 8,
            maxBarThickness: 44,
        },
    ],
}));

const barOptions = {
    plugins: { legend: { display: false } },
    scales: {
        x: {
            ticks: { color: "#94a3b8" },
            grid: { display: false },
        },
        y: {
            beginAtZero: true,
            ticks: { color: "#94a3b8", precision: 0 },
            grid: { color: "rgba(148,163,184,0.08)" },
        },
    },
};

// ===============================
// LINE : TÂCHES CRÉÉES (6 MOIS)
// ===============================

const evolutionData = computed(() => {
    const now = new Date();
    const labels = [];
    const counts = [];

    for (let i = 5; i >= 0; i--) {
        const d = new Date(now.getFullYear(), now.getMonth() - i, 1);

        labels.push(
            d.toLocaleDateString("fr-FR", { month: "short" })
        );

        counts.push(
            tasks.value.filter((t) => {
                const c = new Date(t.created_at);
                return (
                    c.getFullYear() === d.getFullYear() &&
                    c.getMonth() === d.getMonth()
                );
            }).length
        );
    }

    return {
        labels,
        datasets: [
            {
                label: "Tâches créées",
                data: counts,
                borderColor: "#3b82f6",
                backgroundColor: "rgba(59,130,246,0.12)",
                fill: true,
                tension: 0.4,
                pointBackgroundColor: "#3b82f6",
                pointRadius: 4,
            },
        ],
    };
});

const lineOptions = {
    plugins: { legend: { display: false } },
    scales: {
        x: {
            ticks: { color: "#94a3b8" },
            grid: { display: false },
        },
        y: {
            beginAtZero: true,
            ticks: { color: "#94a3b8", precision: 0 },
            grid: { color: "rgba(148,163,184,0.08)" },
        },
    },
};

// ===============================
// ANNEAU DE PROGRESSION
// ===============================

const RING = 2 * Math.PI * 52;

const ringOffset = computed(
    () => RING * (1 - progress.value / 100)
);

onMounted(loadTasks);
</script>

<template>
<div class="statistics-page">

    <header class="page-header anim-fade-up">
        <h1>
            <BarChart3 :size="26" class="page-icon" />
            Statistiques
        </h1>
        <p>Vue d'ensemble de {{ spaceName }}</p>
    </header>


    <div v-if="loading" class="loading">
        <div class="loading-dots"><span></span><span></span><span></span></div>
    </div>


    <template v-else>

        <!-- COMPTEURS -->
        <div class="counters stagger">

            <div class="counter">
                <ClipboardList :size="18" />
                <div>
                    <strong>{{ total }}</strong>
                    <span>tâches</span>
                </div>
            </div>

            <div class="counter">
                <CircleCheck :size="18" class="ok" />
                <div>
                    <strong>{{ done }}</strong>
                    <span>terminées</span>
                </div>
            </div>

            <div class="counter">
                <TriangleAlert :size="18" class="warn" />
                <div>
                    <strong>{{ overdue }}</strong>
                    <span>en retard</span>
                </div>
            </div>

            <div class="counter">
                <Star :size="18" class="fav" />
                <div>
                    <strong>{{ favorites }}</strong>
                    <span>favorites</span>
                </div>
            </div>

        </div>


        <div class="charts">

            <!-- DOUGHNUT -->
            <div class="chart-card anim-fade-up">
                <h3>Répartition par statut</h3>
                <div class="chart-box doughnut-box">
                    <Doughnut
                        :data="statusData"
                        :options="doughnutOptions"
                    />
                    <div class="doughnut-center">
                        <strong>{{ total }}</strong>
                        <span>tâches</span>
                    </div>
                </div>
            </div>


            <!-- BAR -->
            <div class="chart-card anim-fade-up">
                <h3>Priorités</h3>
                <div class="chart-box">
                    <Bar
                        :data="priorityData"
                        :options="barOptions"
                    />
                </div>
            </div>


            <!-- PROGRESSION -->
            <div class="chart-card anim-fade-up">
                <h3>Progression globale</h3>
                <div class="ring-wrap">
                    <svg viewBox="0 0 120 120" class="ring">
                        <circle
                            cx="60" cy="60" r="52"
                            class="ring-bg"
                        />
                        <circle
                            cx="60" cy="60" r="52"
                            class="ring-fill"
                            :stroke-dasharray="RING"
                            :stroke-dashoffset="ringOffset"
                        />
                    </svg>
                    <div class="ring-label">
                        <strong>{{ progress }}%</strong>
                        <span>terminé</span>
                    </div>
                </div>
            </div>


            <!-- EVOLUTION -->
            <div class="chart-card wide anim-fade-up">
                <h3>Tâches créées — 6 derniers mois</h3>
                <div class="chart-box">
                    <Line
                        :data="evolutionData"
                        :options="lineOptions"
                    />
                </div>
            </div>

        </div>

    </template>

</div>
</template>

<style scoped>
.statistics-page {
    min-height: 100vh;
    padding: 32px;
    background: transparent;
    color: var(--text);
}

.page-header {
    margin-bottom: 26px;
}

.page-header h1 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: var(--display);
    font-size: 28px;
    color: var(--text-h);
    margin: 0;
}

.page-icon {
    color: var(--accent);
}

.page-header p {
    margin: 4px 0 0;
    font-size: 13px;
}

.loading {
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* COMPTEURS */

.counters {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 14px;
    margin-bottom: 22px;
}

.counter {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 18px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--accent);
    transition: border-color 0.2s, transform 0.2s;
}

.counter:hover {
    border-color: var(--accent-border);
    transform: translateY(-2px);
}

.counter .ok { color: var(--success); }
.counter .warn { color: var(--danger); }
.counter .fav { color: var(--warning); }

.counter strong {
    display: block;
    font-family: var(--display);
    font-size: 22px;
    color: var(--text-h);
    line-height: 1;
}

.counter span {
    font-size: 11px;
    color: var(--text);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* CARTES */

.charts {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 18px;
}

.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-l);
    padding: 24px;
    transition: border-color 0.25s, transform 0.25s;
}

.chart-card:hover {
    border-color: var(--accent-border);
    transform: translateY(-3px);
}

.chart-card.wide {
    grid-column: 1 / -1;
}

.chart-card h3 {
    color: var(--text-h);
    font-family: var(--display);
    font-size: 16px;
    margin: 0 0 18px;
}

.chart-box {
    height: 260px;
    position: relative;
}

.doughnut-box {
    height: 240px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.doughnut-center {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    padding-bottom: 52px;
}

.doughnut-center strong {
    font-family: var(--display);
    font-size: 30px;
    color: var(--text-h);
}

.doughnut-center span {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text);
}

/* ANNEAU */

.ring-wrap {
    position: relative;
    height: 240px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ring {
    width: 190px;
    transform: rotate(-90deg);
}

.ring-bg {
    fill: none;
    stroke: var(--surface-2);
    stroke-width: 10;
}

.ring-fill {
    fill: none;
    stroke: var(--accent);
    stroke-width: 10;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.8s ease;
}

.ring-label {
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.ring-label strong {
    font-family: var(--display);
    font-size: 34px;
    color: var(--text-h);
}

.ring-label span {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text);
}

/* RESPONSIVE */

@media (max-width: 640px) {
    .statistics-page {
        padding: 16px;
    }

    .chart-box {
        height: 220px;
    }
}
</style>
