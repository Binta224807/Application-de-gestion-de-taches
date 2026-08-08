<template>

<div class="kanban-page">

    <!-- ============================= -->
    <!-- HEADER -->
    <!-- ============================= -->

    <div class="kanban-header">

        <div>

            <h1 class="kanban-title">

                Kanban

            </h1>

            <p class="kanban-subtitle">

                Organisez vos tâches par glisser-déposer.

            </p>

        </div>

        <button

            class="new-task-btn"

            @click="openTaskForm"

        >

            + Nouvelle tâche

        </button>

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
    <!-- KANBAN -->
    <!-- ============================= -->

    <div

        v-else

        class="kanban-board"

    >
    <!-- ===================== -->
<!-- À FAIRE -->
<!-- ===================== -->

        <KanbanColumn
            title="À faire"
            status="todo"
            color="#3B82F6"
            :tasks="todoTasks"
            @taskMoved="moveTask"
            @editTask="editTask"
            @deleteTask="deleteTask"
            @archiveTask="openArchiveModal"
        />


        <!-- ===================== -->
        <!-- EN COURS -->
        <!-- ===================== -->

        <KanbanColumn
            title="En cours"
            status="in_progress"
            color="#F59E0B"
            :tasks="inProgressTasks"
            @taskMoved="moveTask"
            @editTask="editTask"
            @deleteTask="deleteTask"
            @archiveTask="openArchiveModal"
        />


        <!-- ===================== -->
        <!-- TERMINÉE -->
        <!-- ===================== -->

        <KanbanColumn
            title="Terminée"
            status="done"
            color="#22C55E"
            :tasks="doneTasks"
            @taskMoved="moveTask"
            @editTask="editTask"
            @deleteTask="deleteTask"
            @archiveTask="openArchiveModal"
        />
                <!-- ===================== -->
                <!-- TODO -->
                <!-- ===================== -->
                
    </div>
    <TaskForm
    v-if="showTaskForm"
    :task="selectedTask"
    @close="closeTaskForm"
    @saved="reloadTasks"
/>

    <!-- ============================= -->
    <!-- EMPTY -->
    <!-- ============================= -->

    <div

        v-if="

            !loading &&

            todoTasks.length===0 &&

            inProgressTasks.length===0 &&

            doneTasks.length===0

        "

        class="empty-state"

    >

        <h2>

            Aucune tâche

        </h2>

        <p>

            Cliquez sur

            <strong>

                Nouvelle tâche

            </strong>

            pour commencer.

        </p>

    </div>
    <ArchiveModal
        v-if="showArchiveModal && taskToArchive"
        :task="taskToArchive"
        @close="closeArchiveModal"
        @confirmArchive="confirmArchive"
        />
    
</div>

</template>

<script setup>

import { ref, computed, onMounted } from "vue";

import api from "../services/api";

import KanbanColumn from "../components/KanbanColumn.vue";
import Taskcard from "../components/TaskCard.vue";
import TaskForm from "../components/TaskForm.vue";
import ArchiveModal from "../components/ArchiveModal.vue";
import { useSearch } from "../components/useSearch";


const { searchQuery } = useSearch();
// =======================================================
// ETAT
// =======================================================


const loading = ref(true);
const tasks = ref([]);

const selectedTask = ref(null)
const showTaskForm = ref(false);


const showArchiveModal = ref(false);
const taskToArchive = ref(null);


const openArchiveModal = (task) => {
  taskToArchive.value = task;
  showArchiveModal.value = true;
};


// =======================================================
// COLONNES
// =======================================================

const todoTasks = computed(() =>
    tasks.value.filter(task =>
        task.status === "todo" &&
        task.title
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase())
    )
);

const inProgressTasks = computed(() =>
    tasks.value.filter(task =>
        task.status === "in_progress" &&
        task.title
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase())
    )
);



const doneTasks = computed(() =>
    tasks.value.filter(task =>
        task.status === "done" &&
        task.title
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase())
    )
);



// =======================================================
// CHARGEMENT
// =======================================================

const loadTasks = async () => {

    try {

        loading.value = true;

        const response = await api.get(
            "tasks/"
        );
        console.log("TACHES API :", response.data);
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



// =======================================================
// RECHARGER
// =======================================================

const reloadTasks = async () => {

    await loadTasks();

};



// =======================================================
// CREATION
// =======================================================

const openTaskForm = () => {

    selectedTask.value = null;

    showTaskForm.value = true;

};



// =======================================================
// MODIFICATION
// =======================================================

const editTask = (task) => {

    selectedTask.value = task;

    showTaskForm.value = true;

};



// =======================================================
// FERMER
// =======================================================

const closeTaskForm = () => {

    selectedTask.value = null;

    showTaskForm.value = false;

};

const moveTask = async ({ taskId, newStatus }) => {

    try {

        await api.patch(
            `tasks/${taskId}/`,
            {
                status: newStatus
            }
        );


        await loadTasks();


        // =============================
        // Si tâche terminée
        // =============================

       

    }

    catch(error){

        console.error(error);

    }

};

const moveTaskByButton = async ({ task, newStatus }) => {

    // Évite de faire une requête
    // si la tâche est déjà dans cette colonne

    if (task.status === newStatus) {
        return;
    }

    try {

        await api.patch(

            `tasks/${task.id}/`,

            {
                status: newStatus
            }

        );

        await loadTasks();

    }

    catch (error) {

        console.error(
            "Erreur déplacement tâche :",
            error.response?.data || error
        );

    }

};
// =======================================================
// ARCHIVER
// =======================================================

const archiveTask = async (task, duration="30_days") => {

    try {

        await api.post(

            `tasks/${task.id}/archive/`,

            {
                duration: duration
            }

        );

        await loadTasks();

    }

    catch (error) {

        console.error(
            error.response?.data || error
        );

    }

};

const closeArchiveModal = () => {

    showArchiveModal.value = false;

    taskToArchive.value = null;

};



const confirmArchive = async ({ task, duration }) => {


    await archiveTask(
        task,
        duration
    );


    closeArchiveModal();

};

// =======================================================
// SUPPRESSION
// =======================================================

const deleteTask = async (task) => {

    const confirmation = confirm(

        "Supprimer cette tâche ?"

    );

    if (!confirmation) return;

    try {

        await api.delete(

            `tasks/${task.id}/`

        );

        await loadTasks();

    }

    catch (error) {

        console.error(error);

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

.kanban-page {
    padding: 30px;
    min-height: 100vh;
    background: #020617;
}


.kanban-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}


.kanban-title {
    color: white;
    font-size: 32px;
    font-weight: 800;
}


.kanban-subtitle {
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
}


.new-task-btn:hover {
    transform: translateY(-2px);
}


.kanban-board {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
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
}


@media (max-width: 900px) {

    .kanban-board {
        grid-template-columns: 1fr;
    }

    .kanban-header {
        flex-direction: column;
        gap: 20px;
        align-items: flex-start;
    }

}

</style>