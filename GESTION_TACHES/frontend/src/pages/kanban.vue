<template>

<div class="tasks-page">

    <!-- ============================= -->
    <!-- HEADER -->
    <!-- ============================= -->

    <div class="tasks-header">

        <div>
            <h1 class="tasks-title">
                Gestion des tâches
            </h1>

            <p class="tasks-subtitle">
                Liste des tâches de {{ companyName }}
            </p>
        </div>

        <button
            v-if="isCEO"
            class="new-task-btn"
            @click="openTaskForm"
        >
            + Nouvelle tâche
        </button>

    </div>


    <!-- ============================= -->
    <!-- FILTRES -->
    <!-- ============================= -->

    <div class="filters">

        <input
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher une tâche..."
            class="search-input"
        />

        <select
            v-model="statusFilter"
            class="filter-select"
        >
            <option value="">Tous les statuts</option>
            <option value="todo">À faire</option>
            <option value="in_progress">En cours</option>
            <option value="done">Terminées</option>
        </select>

    </div>


    <!-- ============================= -->
    <!-- LOADING -->
    <!-- ============================= -->

    <div
        v-if="loading"
        class="loading-container"
    >
        Chargement...
    </div>


    <!-- ============================= -->
    <!-- LISTE -->
    <!-- ============================= -->

    <div
        v-else
        class="tasks-list"
    >

        <TaskCard
            v-for="task in filteredTasks"
            :key="task.id"
            :task="task"
            @editTask="editTask"
            @deleteTask="deleteTask"
        />

    </div>


    <!-- ============================= -->
    <!-- EMPTY -->
    <!-- ============================= -->

    <div
        v-if="!loading && filteredTasks.length === 0"
        class="empty-state"
    >

        <h2>
            Aucune tâche
        </h2>

        <p>
            {{ isCEO ? "Cliquez sur Nouvelle tâche pour commencer." : "Aucune tâche ne vous est assignée pour le moment." }}
        </p>

    </div>


    <TaskForm
        v-if="showTaskForm"
        :task="selectedTask"
        @close="closeTaskForm"
        @saved="reloadTasks"
    />

</div>

</template>

<script setup>

import { ref, computed, onMounted } from "vue";
import api from "../services/api";

import TaskCard from "../components/TaskCard.vue";
import TaskForm from "../components/TaskForm.vue";


// =======================================================
// ETAT
// =======================================================

const loading = ref(true);
const tasks = ref([]);

const selectedTask = ref(null);
const showTaskForm = ref(false);

const searchQuery = ref("");
const statusFilter = ref("");

const isCEO = ref(localStorage.getItem("is_ceo") === "1");
const companyName = ref(localStorage.getItem("company_name") || "votre entreprise");


// =======================================================
// FILTRES
// =======================================================

const filteredTasks = computed(() => {

    return tasks.value.filter(task => {

        const matchesSearch = task.title
            .toLowerCase()
            .includes(searchQuery.value.toLowerCase());

        const matchesStatus = statusFilter.value === ""
            || task.status === statusFilter.value;

        return matchesSearch && matchesStatus;

    });

});


// =======================================================
// CHARGEMENT
// =======================================================

const loadTasks = async () => {

    try {

        loading.value = true;

        const response = await api.get("tasks/");

        tasks.value = response.data;

    }

    catch (error) {

        console.error(
            error.response?.data || error
        );

    }

    finally {

        loading.value = false;

    }

};


const reloadTasks = async () => {

    await loadTasks();

};


// =======================================================
// CREATION / MODIFICATION
// =======================================================

const openTaskForm = () => {

    selectedTask.value = null;
    showTaskForm.value = true;

};


const editTask = (task) => {

    selectedTask.value = task;
    showTaskForm.value = true;

};


const closeTaskForm = () => {

    selectedTask.value = null;
    showTaskForm.value = false;

};


// =======================================================
// SUPPRESSION VERS CORBEILLE
// =======================================================

const deleteTask = async (task) => {

    const confirmation = confirm("Déplacer cette tâche dans la corbeille ?");

    if (!confirmation) return;

    try {

        await api.delete(`tasks/${task.id}/`);

        await loadTasks();

    }

    catch (error) {

        console.error(
            "Erreur suppression :",
            error.response?.data || error
        );

    }

};


// =======================================================
// INITIALISATION
// =======================================================

onMounted(() => {

    loadTasks();

});


</script>

<style scoped>

.tasks-page {

    padding: 30px;
    min-height: 100vh;
    background: #020617;

}


.tasks-header {

    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    flex-wrap: wrap;
    gap: 16px;

}


.tasks-title {

    color: white;
    font-size: 32px;
    font-weight: 800;

}


.tasks-subtitle {

    color: #94a3b8;
    margin-top: 8px;

}


.new-task-btn {

    background: #2563eb;
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: .2s;

}


.new-task-btn:hover {

    transform: translateY(-2px);
    background: #1d4ed8;

}


.filters {

    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    flex-wrap: wrap;

}


.search-input,
.filter-select {

    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid #334155;
    background: #1e293b;
    color: white;
    font-size: 14px;
    outline: none;

}


.search-input {

    flex: 1;
    min-width: 220px;

}


.filter-select {

    min-width: 180px;

}


.search-input:focus,
.filter-select:focus {

    border-color: #2563eb;

}


.tasks-list {

    display: flex;
    flex-direction: column;
    gap: 14px;

}


.loading-container {

    color: white;
    text-align: center;
    padding: 50px;

}


.empty-state {

    text-align: center;
    color: #94a3b8;
    margin-top: 40px;
    padding: 40px;
    background: #1e293b;
    border-radius: 20px;
    border: 1px solid #334155;

}


@media (max-width: 768px) {

    .tasks-page {

        padding: 18px;

    }

    .tasks-title {

        font-size: 26px;

    }

    .tasks-header {

        flex-direction: column;
        align-items: flex-start;

    }

    .new-task-btn {

        width: 100%;

    }

    .filters {

        flex-direction: column;

    }

    .search-input,
    .filter-select {

        width: 100%;
        box-sizing: border-box;

    }

}

</style>
