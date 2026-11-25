<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import {
    CalendarDays,
    ChevronLeft,
    ChevronRight,
    Clock,
    Folder,
    User,
} from "lucide-vue-next";

const router = useRouter();

const tasks = ref([]);
const loading = ref(true);
const currentDate = ref(new Date());
const selectedDay = ref(null);

const WEEKDAYS = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"];

const PRIORITY_COLORS = {
    low: "#22c55e",
    medium: "#f59e0b",
    high: "#ef4444",
    urgent: "#dc2626",
};

const STATUS_LABELS = {
    todo: "À faire",
    in_progress: "En cours",
    review: "À vérifier",
    done: "Terminée",
};

const loadCalendar = async () => {
    try {
        loading.value = true;
        const response = await api.get("calendar/");
        tasks.value = response.data;
    } catch (error) {
        console.error("Erreur calendrier :", error);
    } finally {
        loading.value = false;
    }
};

const monthName = computed(() =>
    currentDate.value.toLocaleDateString("fr-FR", {
        month: "long",
        year: "numeric",
    })
);

// Date locale YYYY-MM-DD (évite le décalage UTC de toISOString)
const localISO = (d) =>
    `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(
        d.getDate()
    ).padStart(2, "0")}`;

const todayISO = localISO(new Date());

// Cellules : cases vides (décalage lundi) + jours du mois
const cells = computed(() => {
    const year = currentDate.value.getFullYear();
    const month = currentDate.value.getMonth();

    const firstDay = new Date(year, month, 1);
    const offset = (firstDay.getDay() + 6) % 7;
    const total = new Date(year, month + 1, 0).getDate();

    const result = Array(offset).fill(null);

    for (let i = 1; i <= total; i++) {
        result.push(new Date(year, month, i));
    }

    return result;
});

const tasksByDay = (day) => {
    if (!day) return [];
    const iso = localISO(day);
    return tasks.value.filter((t) => t.date === iso);
};

const isToday = (day) => day && localISO(day) === todayISO;

const isSelected = (day) =>
    day && selectedDay.value && localISO(day) === localISO(selectedDay.value);

const selectDay = (day) => {
    if (!day) return;
    selectedDay.value = isSelected(day) ? null : day;
};

const selectedTasks = computed(() =>
    selectedDay.value ? tasksByDay(selectedDay.value) : []
);

const selectedLabel = computed(() =>
    selectedDay.value?.toLocaleDateString("fr-FR", {
        weekday: "long",
        day: "numeric",
        month: "long",
    })
);

const previousMonth = () => {
    currentDate.value = new Date(
        currentDate.value.getFullYear(),
        currentDate.value.getMonth() - 1,
        1
    );
    selectedDay.value = null;
};

const nextMonth = () => {
    currentDate.value = new Date(
        currentDate.value.getFullYear(),
        currentDate.value.getMonth() + 1,
        1
    );
    selectedDay.value = null;
};

const goToday = () => {
    currentDate.value = new Date();
    selectedDay.value = new Date();
};

const goTask = (id) => router.push(`/tasks/${id}`);

const monthTaskCount = computed(() => {
    const y = currentDate.value.getFullYear();
    const m = currentDate.value.getMonth();
    return tasks.value.filter((t) => {
        const d = new Date(t.date + "T00:00:00");
        return d.getFullYear() === y && d.getMonth() === m;
    }).length;
});

onMounted(() => {
    loadCalendar();
    selectedDay.value = new Date();
});
</script>

<template>
<div class="calendar-page">

    <!-- HEADER -->
    <div class="calendar-header anim-fade-up">

        <div>
            <h1>
                <CalendarDays :size="26" class="page-icon" />
                Calendrier
            </h1>
            <p>
                {{ monthTaskCount }} échéance{{ monthTaskCount > 1 ? "s" : "" }}
                ce mois-ci
            </p>
        </div>


        <div class="navigation">

            <button class="nav-btn" @click="previousMonth" aria-label="Mois précédent">
                <ChevronLeft :size="18" />
            </button>

            <h2>{{ monthName }}</h2>

            <button class="nav-btn" @click="nextMonth" aria-label="Mois suivant">
                <ChevronRight :size="18" />
            </button>

            <button class="today-btn" @click="goToday">
                Aujourd'hui
            </button>

        </div>

    </div>


    <!-- LOADING -->
    <div v-if="loading" class="loading">
        <div class="loading-dots"><span></span><span></span><span></span></div>
    </div>


    <template v-else>

        <!-- JOURS DE LA SEMAINE -->
        <div class="weekdays">
            <span v-for="w in WEEKDAYS" :key="w">{{ w }}</span>
        </div>


        <!-- GRILLE -->
        <div class="calendar-grid anim-fade-up">

            <div
                v-for="(day, i) in cells"
                :key="i"
                class="day-cell"
                :class="{
                    empty: !day,
                    today: isToday(day),
                    selected: isSelected(day),
                    'has-tasks': day && tasksByDay(day).length,
                }"
                @click="selectDay(day)"
            >
                <template v-if="day">

                    <span class="day-number">{{ day.getDate() }}</span>

                    <div class="dots">
                        <span
                            v-for="t in tasksByDay(day).slice(0, 3)"
                            :key="t.id"
                            class="dot"
                            :style="{
                                background:
                                    PRIORITY_COLORS[t.priority] ||
                                    PRIORITY_COLORS.medium,
                            }"
                        />
                        <span
                            v-if="tasksByDay(day).length > 3"
                            class="more"
                        >+{{ tasksByDay(day).length - 3 }}</span>
                    </div>

                </template>
            </div>

        </div>


        <!-- TÂCHES DU JOUR SÉLECTIONNÉ -->
        <section v-if="selectedDay" class="day-panel anim-fade-up">

            <h3>{{ selectedLabel }}</h3>

            <div v-if="!selectedTasks.length" class="empty-day">
                Aucune échéance ce jour.
            </div>

            <div v-else class="day-tasks">

                <button
                    v-for="task in selectedTasks"
                    :key="task.id"
                    class="day-task"
                    @click="goTask(task.id)"
                >
                    <span
                        class="task-priority"
                        :style="{
                            background:
                                PRIORITY_COLORS[task.priority] ||
                                PRIORITY_COLORS.medium,
                        }"
                    />

                    <span class="task-name">{{ task.title }}</span>

                    <span class="task-meta">
                        <Clock :size="12" />
                        {{ task.time ? task.time.slice(0, 5) : "—" }}
                    </span>

                    <span v-if="task.project" class="task-meta">
                        <Folder :size="12" />
                        {{ task.project }}
                    </span>

                    <span v-if="task.assigned_to" class="task-meta">
                        <User :size="12" />
                        {{ task.assigned_to }}
                    </span>

                    <span class="status-chip" :class="task.status">
                        {{ STATUS_LABELS[task.status] || task.status }}
                    </span>

                </button>

            </div>

        </section>

    </template>

</div>
</template>

<style scoped>
.calendar-page {
    min-height: 100vh;
    padding: 32px;
    background: transparent;
    color: var(--text);
}

/* HEADER */

.calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 26px;
}

.calendar-header h1 {
    font-family: var(--display);
    font-size: 28px;
    font-weight: 700;
    color: var(--text-h);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.page-icon {
    color: var(--accent);
}

.calendar-header p {
    margin: 4px 0 0;
    font-size: 13px;
}

/* NAVIGATION */

.navigation {
    display: flex;
    align-items: center;
    gap: 8px;
}

.navigation h2 {
    font-family: var(--display);
    text-transform: capitalize;
    font-size: 19px;
    color: var(--text-h);
    margin: 0 8px;
    min-width: 140px;
    text-align: center;
}

.nav-btn {
    width: 38px;
    height: 38px;
    border: 1px solid var(--border-strong);
    border-radius: 11px;
    background: var(--surface);
    color: var(--text-h);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: 0.2s;
}

.nav-btn:hover {
    border-color: var(--accent-border);
    color: var(--accent);
    transform: translateY(-2px);
}

.today-btn {
    margin-left: 6px;
    border: 1px solid var(--accent-border);
    border-radius: 11px;
    background: var(--accent-soft);
    color: var(--accent);
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    padding: 9px 16px;
    cursor: pointer;
    transition: 0.2s;
}

.today-btn:hover {
    background: var(--accent-strong);
    color: white;
}

/* LOADING */

.loading {
    height: 300px;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* SEMAINE */

.weekdays {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
    margin-bottom: 8px;
}

.weekdays span {
    text-align: center;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text);
    padding: 6px 0;
}

/* GRILLE */

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
}

.day-cell {
    position: relative;
    min-height: 88px;
    padding: 10px;
    border-radius: var(--radius-s);
    background: var(--surface);
    border: 1px solid var(--border);
    cursor: pointer;
    transition: border-color 0.2s, transform 0.2s, background 0.2s;
}

.day-cell.empty {
    background: transparent;
    border-color: transparent;
    cursor: default;
    min-height: 0;
}

.day-cell:not(.empty):hover {
    border-color: var(--accent-border);
    transform: translateY(-2px);
}

.day-cell.today {
    border-color: var(--accent);
    background: var(--accent-soft);
}

.day-cell.today .day-number {
    color: var(--accent);
    font-weight: 800;
}

.day-cell.selected {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-soft);
}

.day-number {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-h);
}

.dots {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-top: 10px;
    flex-wrap: wrap;
}

.dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
}

.more {
    font-size: 10px;
    color: var(--text);
    font-weight: 700;
}

/* PANNEAU DU JOUR */

.day-panel {
    margin-top: 24px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-l);
    padding: 22px;
}

.day-panel h3 {
    margin: 0 0 16px;
    font-family: var(--display);
    text-transform: capitalize;
    color: var(--text-h);
    font-size: 18px;
}

.empty-day {
    color: var(--text);
    font-size: 14px;
    padding: 10px 0;
}

.day-tasks {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.day-task {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 12px;
    cursor: pointer;
    font-family: inherit;
    color: var(--text-h);
    text-align: left;
    transition: border-color 0.2s, transform 0.2s;
}

.day-task:hover {
    border-color: var(--accent-border);
    transform: translateX(4px);
}

.task-priority {
    width: 4px;
    height: 28px;
    border-radius: 4px;
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

.status-chip {
    margin-left: auto;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.06);
    white-space: nowrap;
}

.status-chip.todo { color: #60a5fa; }
.status-chip.in_progress { color: #fbbf24; }
.status-chip.review { color: #a78bfa; }
.status-chip.done { color: #4ade80; }

/* RESPONSIVE */

@media (max-width: 768px) {
    .calendar-page {
        padding: 16px;
    }

    .calendar-header {
        flex-direction: column;
        align-items: stretch;
    }

    .navigation {
        justify-content: space-between;
    }

    .navigation h2 {
        min-width: 0;
        font-size: 17px;
    }

    .day-cell {
        min-height: 52px;
        padding: 6px;
        border-radius: 8px;
    }

    .day-number {
        font-size: 12px;
    }

    .dots {
        margin-top: 5px;
        gap: 4px;
    }

    .day-task {
        flex-wrap: wrap;
        gap: 8px;
    }

    .status-chip {
        margin-left: 0;
    }
}
</style>
