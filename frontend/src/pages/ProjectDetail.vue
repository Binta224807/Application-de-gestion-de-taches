<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import {
    ArrowLeft,
    ClipboardList,
    CircleCheck,
    Hourglass,
    TriangleAlert,
    Star,
    CalendarDays,
    User,
    Trash2,
} from "lucide-vue-next";

const route = useRoute();
const router = useRouter();

const project = ref(null);
const tasks = ref([]);
const loading = ref(true);
const statusFilter = ref("");

const STATUS_LABELS = {
    todo: "À faire",
    in_progress: "En cours",
    review: "À vérifier",
    done: "Terminée",
};

const STATUS_COLORS = {
    todo: "#3b82f6",
    in_progress: "#d97706",
    review: "#8b5cf6",
    done: "#16a34a",
};

const PRIORITY_LABELS = {
    low: "Faible",
    medium: "Moyenne",
    high: "Élevée",
    urgent: "Urgente",
};

const loadAll = async () => {
    try {
        loading.value = true;

        const [p, t] = await Promise.all([
            api.get(`projects/${route.params.id}/`),
            api.get(`tasks/?project=${route.params.id}`),
        ]);

        project.value = p.data;
        tasks.value = t.data;
    } catch (error) {
        console.error(error);
    } finally {
        loading.value = false;
    }
};

const count = (s) => tasks.value.filter((t) => t.status === s).length;

const done = computed(() => count("done"));
const inProgress = computed(() => count("in_progress"));
const overdue = computed(() => tasks.value.filter((t) => t.is_overdue).length);

const progress = computed(() => {
    if (!tasks.value.length) return 0;
    return Math.round((done.value / tasks.value.length) * 100);
});

const filteredTasks = computed(() =>
    statusFilter.value
        ? tasks.value.filter((t) => t.status === statusFilter.value)
        : tasks.value
);

const goTask = (id) => router.push(`/tasks/${id}`);

const deleteProject = async () => {
    const n = tasks.value.length;
    const info = n
        ? ` Ses ${n} tâche(s) seront conservées sans projet.`
        : "";

    if (!confirm(`Supprimer le projet « ${project.value.name} » ?${info}`)) {
        return;
    }

    try {
        await api.delete(`projects/${project.value.id}/`);
        router.push("/projects");
    } catch (error) {
        console.error("Erreur suppression projet :", error);
    }
};

onMounted(loadAll);
</script>

<template>
<div class="project-page">

    <button class="back-btn" @click="router.back()">
        <ArrowLeft :size="15" /> Retour
    </button>


    <div v-if="loading" class="loading">
        <div class="loading-dots"><span></span><span></span><span></span></div>
    </div>


    <template v-else-if="project">

        <!-- HEADER -->
        <header class="project-header anim-fade-up">

            <div class="project-title">

                <span
                    class="project-icon"
                    :style="{ background: (project.color || '#6366f1') + '22' }"
                >
                    {{ project.icon || "📁" }}
                </span>

                <div>
                    <h1>{{ project.name }}</h1>
                    <p>{{ project.description || "Aucune description" }}</p>
                </div>

            </div>

            <div class="header-side">

                <span v-if="project.is_favorite" class="favorite">
                    <Star :size="14" /> Favori
                </span>

                <button class="delete-btn" @click="deleteProject">
                    <Trash2 :size="14" /> Supprimer
                </button>

            </div>

        </header>


        <!-- PROGRESSION -->
        <section class="progress-card anim-fade-up">

            <div class="progress-top">
                <h2>Progression du projet</h2>
                <strong
                    class="progress-pct"
                    :style="{ color: project.color || 'var(--accent)' }"
                >
                    {{ progress }}%
                </strong>
            </div>

            <div class="progress-bar">
                <span
                    class="progress-fill"
                    :style="{
                        width: progress + '%',
                        background: project.color || 'var(--accent)',
                    }"
                />
            </div>

            <div class="progress-legend">
                {{ done }}/{{ tasks.length }} tâches terminées
            </div>

            <div class="mini-stats stagger">

                <div class="mini-stat">
                    <ClipboardList :size="15" />
                    <strong>{{ tasks.length }}</strong>
                    <span>Total</span>
                </div>

                <div class="mini-stat done">
                    <CircleCheck :size="15" />
                    <strong>{{ done }}</strong>
                    <span>Terminées</span>
                </div>

                <div class="mini-stat running">
                    <Hourglass :size="15" />
                    <strong>{{ inProgress }}</strong>
                    <span>En cours</span>
                </div>

                <div class="mini-stat late">
                    <TriangleAlert :size="15" />
                    <strong>{{ overdue }}</strong>
                    <span>En retard</span>
                </div>

            </div>

        </section>


        <!-- FILTRE STATUT -->
        <div class="status-filters">

            <button
                :class="{ active: statusFilter === '' }"
                @click="statusFilter = ''"
            >
                Toutes ({{ tasks.length }})
            </button>

            <button
                v-for="(label, key) in STATUS_LABELS"
                :key="key"
                :class="{ active: statusFilter === key }"
                @click="statusFilter = key"
            >
                {{ label }} ({{ count(key) }})
            </button>

        </div>


        <!-- TÂCHES -->
        <div v-if="filteredTasks.length" class="task-list">

            <button
                v-for="task in filteredTasks"
                :key="task.id"
                class="task-row"
                @click="goTask(task.id)"
            >
                <span
                    class="status-dot"
                    :style="{ background: STATUS_COLORS[task.status] }"
                />

                <span class="task-name">{{ task.title }}</span>

                <span
                    v-if="task.assigned_to?.length"
                    class="task-meta"
                >
                    <User :size="12" />
                    {{ task.assigned_to.map(u => u.username).join(", ") }}
                </span>

                <span v-if="task.due_date" class="task-meta">
                    <CalendarDays :size="12" /> {{ task.due_date }}
                </span>

                <span class="task-priority">{{ PRIORITY_LABELS[task.priority] }}</span>

                <span
                    class="status-chip"
                    :style="{
                        color: STATUS_COLORS[task.status],
                        background: STATUS_COLORS[task.status] + '1f',
                    }"
                >
                    {{ STATUS_LABELS[task.status] || task.status }}
                </span>

                <div class="task-progress">
                    <span
                        :style="{
                            width: (task.progress || 0) + '%',
                            background: STATUS_COLORS[task.status],
                        }"
                    />
                </div>

            </button>

        </div>


        <div v-else class="empty">
            Aucune tâche{{ statusFilter ? " avec ce statut" : "" }} dans ce projet.
        </div>

    </template>


    <div v-else class="empty">Projet introuvable.</div>

</div>
</template>

<style scoped>
.project-page {
    min-height: 100vh;
    padding: 32px;
    background: transparent;
    color: var(--text);
}

.back-btn {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: none;
    border: none;
    color: var(--text);
    font-family: inherit;
    font-size: 14px;
    cursor: pointer;
    padding: 0;
    margin-bottom: 22px;
    transition: color 0.2s;
}

.back-btn:hover {
    color: var(--text-h);
}

.loading {
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* HEADER */

.project-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 22px;
}

.project-title {
    display: flex;
    align-items: center;
    gap: 16px;
}

.project-icon {
    width: 56px;
    height: 56px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    flex-shrink: 0;
}

.project-title h1 {
    font-family: var(--display);
    font-size: 26px;
    color: var(--text-h);
    margin: 0;
}

.project-title p {
    margin: 4px 0 0;
    font-size: 13px;
}

.header-side {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
}

.favorite {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: var(--warning);
    font-size: 12px;
    font-weight: 700;
    background: rgba(245, 158, 11, 0.12);
    padding: 6px 12px;
    border-radius: 999px;
    white-space: nowrap;
}

.delete-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-radius: 10px;
    background: rgba(239, 68, 68, 0.1);
    color: var(--danger);
    font-family: inherit;
    font-size: 12px;
    font-weight: 700;
    padding: 8px 14px;
    cursor: pointer;
    transition: 0.2s;
}

.delete-btn:hover {
    background: var(--danger);
    color: white;
}

/* PROGRESSION */

.progress-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-l);
    padding: 24px;
    margin-bottom: 22px;
}

.progress-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}

.progress-top h2 {
    font-family: var(--display);
    font-size: 17px;
    color: var(--text-h);
    margin: 0;
}

.progress-pct {
    font-family: var(--display);
    font-size: 30px;
    font-weight: 700;
}

.progress-bar {
    height: 10px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
}

.progress-fill {
    display: block;
    height: 100%;
    border-radius: 10px;
    transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.progress-legend {
    margin-top: 10px;
    font-size: 12px;
    color: var(--text);
}

.mini-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
    gap: 12px;
    margin-top: 18px;
}

.mini-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 14px 10px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 12px;
    color: var(--accent);
}

.mini-stat.done { color: var(--success); }
.mini-stat.running { color: var(--warning); }
.mini-stat.late { color: var(--danger); }

.mini-stat strong {
    font-family: var(--display);
    font-size: 20px;
    color: var(--text-h);
}

.mini-stat span {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text);
}

/* FILTRES */

.status-filters {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 16px;
}

.status-filters button {
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    font-family: inherit;
    font-size: 12px;
    font-weight: 600;
    padding: 8px 14px;
    border-radius: 999px;
    cursor: pointer;
    transition: 0.2s;
}

.status-filters button:hover {
    border-color: var(--accent-border);
    color: var(--text-h);
}

.status-filters button.active {
    background: var(--accent-soft);
    border-color: var(--accent-border);
    color: var(--accent);
}

/* TÂCHES */

.task-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.task-row {
    position: relative;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    cursor: pointer;
    font-family: inherit;
    color: var(--text-h);
    text-align: left;
    transition: border-color 0.2s, transform 0.2s;
    overflow: hidden;
}

.task-row:hover {
    border-color: var(--accent-border);
    transform: translateX(4px);
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.task-name {
    font-size: 14px;
    font-weight: 600;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.task-meta {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    color: var(--text);
    white-space: nowrap;
}

.task-priority {
    font-size: 10px;
    color: var(--text);
    text-transform: uppercase;
    letter-spacing: 0.4px;
    white-space: nowrap;
}

.status-chip {
    margin-left: auto;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 4px 10px;
    border-radius: 999px;
    white-space: nowrap;
}

.task-progress {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 3px;
    background: rgba(255, 255, 255, 0.05);
}

.task-progress span {
    display: block;
    height: 100%;
    transition: width 0.4s ease;
}

.empty {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-l);
    padding: 40px;
    text-align: center;
    color: var(--text);
}

/* RESPONSIVE */

@media (max-width: 640px) {
    .project-page {
        padding: 16px;
    }

    .project-title h1 {
        font-size: 21px;
    }

    .project-icon {
        width: 46px;
        height: 46px;
        font-size: 21px;
        border-radius: 12px;
    }

    .task-row {
        flex-wrap: wrap;
        gap: 8px;
    }

    .status-chip {
        margin-left: 0;
    }
}
</style>
