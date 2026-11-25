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
            <Plus :size="17" /> Nouvelle tâche
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
        <div class="loading-dots"><span></span><span></span><span></span></div>
        <p>Chargement...</p>
    </div>


    <!-- ============================= -->
    <!-- LISTE -->
    <!-- ============================= -->

    <div
        v-else
        class="tasks-list stagger"
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


    <Transition name="modal">

        <TaskForm
            v-if="showTaskForm"
            :task="selectedTask"
            @close="closeTaskForm"
            @saved="reloadTasks"
        />

    </Transition>

</div>

</template>

<script setup>

import { ref, computed, onMounted } from "vue";
import api from "../services/api";

import TaskCard from "../components/TaskCard.vue";
import TaskForm from "../components/TaskForm.vue";
import { Plus } from "lucide-vue-next";


// =======================================================
// ETAT
// =======================================================

const loading = ref(true);
const tasks = ref([]);

const selectedTask = ref(null);
const showTaskForm = ref(false);

const searchQuery = ref("");
const statusFilter = ref("");

import { isAdmin, spaceName } from "../services/space";
const isCEO = isAdmin;
const companyName = spaceName;


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
    background: transparent;

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

    color: var(--text-h);
    font-size: 32px;
    font-weight: 800;

}


.tasks-subtitle {

    color: var(--text);
    margin-top: 8px;

}


.new-task-btn {

    background: var(--accent-strong);
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: .2s;

    display: inline-flex;
    align-items: center;
    gap: 8px;

}


.new-task-btn {

    position: relative;

    overflow: hidden;

}


.new-task-btn::after {

    content: "";

    position: absolute;

    top: 0;

    left: -80%;

    width: 55%;

    height: 100%;

    background: linear-gradient(
        105deg,
        transparent,
        rgba(255, 255, 255, .22),
        transparent
    );

    transform: skewX(-20deg);

    animation: shine-sweep 3.2s ease-in-out infinite;

}


.new-task-btn:hover {

    transform: translateY(-3px);
    background: var(--accent);

    box-shadow: 0 10px 26px rgba(59, 130, 246, .35);

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
    border: 1px solid var(--border);
    background: var(--surface-2);
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

    border-color: var(--accent);

}


.tasks-list {

    display: flex;
    flex-direction: column;
    gap: 14px;

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


.empty-state {

    text-align: center;
    color: var(--text);
    margin-top: 40px;
    padding: 40px;
    background: var(--surface);
    border-radius: 20px;
    border: 1px solid var(--border);

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
        align-items: stretch;
        padding: 18px;

    }


    .tasks-title {

        font-size: 24px;

    }


    .new-task-btn {

        justify-content: center;
        min-height: 46px;

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


    .tasks-list {

        gap: 8px;

    }


    .tasks-page {

        padding: 14px;

    }

}

</style>
