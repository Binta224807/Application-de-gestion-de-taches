<template>

<div class="dashboard">

    <!-- HEADER -->

    <div class="dashboard-header">

        <div>
            <h1 class="dashboard-title">
                Tableau de bord
            </h1>
            <p class="dashboard-subtitle">
                {{ isCEO ? "Pilotage de " + companyName : "Vos tâches" }}
            </p>
        </div>

    </div>


    <!-- LOADING -->

    <div
        v-if="loading"
        class="loading-container"
    >
        <div class="spinner"></div>
        <p>Chargement des données...</p>
    </div>


    <!-- CONTENT -->

    <template v-else>

        <!-- STATS PRINCIPALES -->

        <div class="stats-grid stagger">

            <StatCard
                title="Total des tâches"
                :icon="ClipboardList"
                :value="dashboard.total_tasks"
            />

            <StatCard
                title="À faire"
                :icon="FileEdit"
                :value="dashboard.todo_tasks"
            />

            <StatCard
                title="En cours"
                :icon="Hourglass"
                :value="dashboard.in_progress_tasks"
            />

            <StatCard
                title="Terminées"
                :icon="CircleCheck"
                :value="dashboard.done_tasks"
            />

            <StatCard
                title="En retard"
                :icon="TriangleAlert"
                :value="dashboard.overdue_tasks"
            />

            <StatCard
                title="Progression moyenne"
                :icon="Target"
                :value="Math.round(dashboard.average_progress) + '%'"
            />

        </div>


        <!-- TABLE PAR EMPLOYÉ (PDG) -->

        <section
            v-if="isCEO"
            class="dashboard-section anim-fade-up"
        >

            <h2><Users :size="19" class="section-icon" /> Vue par employé</h2>

            <div class="employees-table-wrapper">

                <table class="employees-table">

                    <thead>

                        <tr>
                            <th>Employé</th>
                            <th>À faire</th>
                            <th>En cours</th>
                            <th>Terminées</th>
                            <th>En retard</th>
                            <th>Total</th>
                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="employee in employeesStats"
                            :key="employee.id"
                            class="employee-row"
                            @click="goToEmployeeTasks(employee.id)"
                        >

                            <td class="employee-name">
                                {{ employee.username }}
                            </td>

                            <td>{{ employee.todo }}</td>
                            <td>{{ employee.in_progress }}</td>
                            <td>{{ employee.done }}</td>
                            <td>{{ employee.overdue }}</td>
                            <td>{{ employee.total }}</td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </section>


        <!-- TÂCHES RÉCENTES -->

        <div class="dashboard-columns">

            <div class="column stagger">

                <section class="dashboard-section">

                    <h2><Flame :size="19" class="section-icon" /> Tâches urgentes</h2>

                    <ActivityList :tasks="urgentTasks" />

                </section>


                <section class="dashboard-section">

                    <h2><TriangleAlert :size="19" class="section-icon" /> Tâches en retard</h2>

                    <ActivityList :tasks="overdueTasks" />

                </section>

            </div>


            <div class="column stagger">

                <section class="dashboard-section">

                    <h2><CalendarClock :size="19" class="section-icon" /> Prochaines échéances</h2>

                    <ActivityList :tasks="upcomingTasks" />

                </section>

            </div>

        </div>

    </template>


</div>

</template>


<script setup>

import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

import StatCard from "../components/StatCard.vue";
import ActivityList from "../components/ActivityList.vue";

import {
    ClipboardList,
    FileEdit,
    Hourglass,
    CircleCheck,
    TriangleAlert,
    Target,
    Users,
    Flame,
    CalendarClock,
} from "lucide-vue-next";

const router = useRouter();

const loading = ref(true);

const dashboard = ref({
    total_tasks: 0,
    todo_tasks: 0,
    in_progress_tasks: 0,
    review_tasks: 0,
    done_tasks: 0,
    overdue_tasks: 0,
    archived_tasks: 0,
    average_progress: 0,
});

const employeesStats = ref([]);
const urgentTasks = ref([]);
const overdueTasks = ref([]);
const upcomingTasks = ref([]);

const isCEO = ref(localStorage.getItem("is_ceo") === "1");
const companyName = ref(localStorage.getItem("company_name") || "votre entreprise");


const loadDashboard = async () => {

    try {

        const response = await api.get("dashboard/");

        const data = response.data;

        dashboard.value = {
            ...dashboard.value,
            ...data.stats,
        };

        employeesStats.value = data.employees_stats || [];

        upcomingTasks.value = data.upcoming_tasks || [];

    }

    catch (error) {

        console.error("Erreur Dashboard :", error.response?.data || error);

    }

};


const loadUrgentTasks = async () => {

    try {

        const response = await api.get("tasks/?priority=urgent");

        urgentTasks.value = response.data;

    }

    catch (error) {

        console.error(error);

    }

};


const loadOverdueTasks = async () => {

    try {

        const response = await api.get("tasks/?overdue=true");

        overdueTasks.value = response.data;

    }

    catch (error) {

        console.error(error);

    }

};


const loadDashboardData = async () => {

    loading.value = true;

    await Promise.all([
        loadDashboard(),
        loadUrgentTasks(),
        loadOverdueTasks(),
    ]);

    loading.value = false;

};


const goToEmployeeTasks = (employeeId) => {

    router.push(`/tasks?assigned=${employeeId}`);

};


onMounted(() => {

    loadDashboardData();

});


</script>


<style scoped>

.dashboard {

    padding: 32px;
    min-height: 100vh;
    background: var(--bg);
    display: flex;
    flex-direction: column;
    gap: 32px;

}


.dashboard-header {

    display: flex;
    justify-content: space-between;
    align-items: center;

}


.dashboard-title {

    color: var(--text-h);
    font-size: 32px;
    font-weight: 800;

}


.dashboard-subtitle {

    color: var(--text);
    margin-top: 8px;

}


.stats-grid {

    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 20px;

}


.dashboard-section {

    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;

}


.dashboard-section h2 {

    color: var(--text-h);
    margin-bottom: 20px;
    font-size: 20px;

}


.employees-table-wrapper {

    overflow-x: auto;

}


.employees-table {

    width: 100%;
    border-collapse: collapse;
    min-width: 500px;

}


.employees-table th,
.employees-table td {

    padding: 14px 16px;
    text-align: left;
    border-bottom: 1px solid var(--border);

}


.employees-table th {

    color: var(--text);
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;

}


.employees-table td {

    color: var(--text-strong);
    font-size: 15px;

}


.employee-row {

    cursor: pointer;
    transition: .2s;

}


.employee-row:hover {

    background: var(--accent-soft);

}


.employee-name {

    color: var(--text-h);
    font-weight: 600;

}


.dashboard-columns {

    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;

}


.column {

    display: flex;
    flex-direction: column;
    gap: 24px;

}


.loading-container {

    color: var(--text);
    text-align: center;
    padding: 50px;

    display: flex;

    flex-direction: column;

    align-items: center;

    gap: 16px;

}


@media (max-width: 1024px) {

    .dashboard-columns {

        grid-template-columns: 1fr;

    }

}


@media (max-width: 768px) {

    .dashboard {

        padding: 18px 14px;
        gap: 20px;

    }

    .dashboard-title {

        font-size: 26px;

    }

    .stats-grid {

        grid-template-columns: 1fr 1fr;
        gap: 12px;

    }

    .dashboard-section {

        padding: 16px;

    }

    .employees-table th,
    .employees-table td {

        padding: 10px 12px;
        font-size: 13px;

    }

}


@media (max-width: 480px) {

    .stats-grid {

        grid-template-columns: 1fr;

    }

}

</style>
