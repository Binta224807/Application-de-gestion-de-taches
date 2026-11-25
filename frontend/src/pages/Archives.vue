<script setup>
import { Hourglass, Trash2, RotateCcw, User, CalendarX } from "lucide-vue-next";

import { ref, onMounted } from "vue";
import api from "../services/api";
import { formatDuration } from "../services/formatDuration.js";

const tasks = ref([]);
const loading = ref(true);
const deleting = ref(null);


const loadTrash = async () => {

    try {

        loading.value = true;

        const response = await api.get("trash/");

        tasks.value = response.data;

    }

    catch (error) {

        console.error("Erreur corbeille :", error.response?.data || error);

    }

    finally {

        loading.value = false;

    }

};


const restoreTask = async (task) => {

    try {

        await api.post(`tasks/${task.id}/restore/`);

        tasks.value = tasks.value.filter(
            item => item.id !== task.id
        );

    }

    catch (error) {

        console.error("Erreur restauration :", error.response?.data || error);

    }

};


const deleteTask = async (task) => {

    const confirmDelete = window.confirm(
        "Supprimer définitivement cette tâche ? Cette action est irréversible."
    );

    if (!confirmDelete) return;

    try {

        deleting.value = task.id;

        await api.delete(`tasks/${task.id}/hard-delete/`);

        tasks.value = tasks.value.filter(
            item => item.id !== task.id
        );

    }

    catch (error) {

        console.error("Erreur suppression :", error.response?.data || error);

    }

    finally {

        deleting.value = null;

    }

};


const formatDate = (date) => {

    if (!date) return "Non définie";

    return new Date(date).toLocaleDateString("fr-FR", {
        day: "2-digit",
        month: "long",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });

};


const assignedName = (task) => {

    const assignees = task.assigned_to || [];

    if (!assignees.length) {

        return "Non assigné";

    }

    return assignees
        .map((u) => u.username)
        .join(", ");

};


onMounted(() => {

    loadTrash();

});


</script>


<template>

<div class="trash-page">

    <!-- HEADER -->

    <div class="trash-header">

        <div>
            <h1><Trash2 :size="26" class="page-icon" /> Corbeille</h1>
            <p>Retrouvez les tâches supprimées.</p>
        </div>

        <div class="count">
            {{ tasks.length }} tâche(s)
        </div>

    </div>


    <!-- LOADING -->

    <div
        v-if="loading"
        class="loading"
    >
        Chargement de la corbeille...
    </div>


    <!-- VIDE -->

    <div
        v-else-if="!tasks.length"
        class="empty"
    >

        <Trash2 :size="52" class="empty-icon" />
        <h2>Corbeille vide</h2>
        <p>Les tâches supprimées apparaîtront ici.</p>

    </div>


    <!-- LISTE -->

    <div
        v-else
        class="trash-list"
    >

        <div
            v-for="task in tasks"
            :key="task.id"
            class="trash-row"
        >

            <div class="row-main">

                <h3>{{ task.title }}</h3>

                <div class="row-meta">

                    <span class="status-badge">
                        {{ task.status }}
                    </span>

                    <span class="meta-item">
                        <User :size="13" /> {{ assignedName(task) }}
                    </span>

                    <span class="meta-item">
                        <Hourglass :size="13" /> {{ formatDuration(task.estimated_duration) }}
                    </span>

                    <span class="meta-item">
                        <CalendarX :size="13" /> {{ formatDate(task.deleted_at) }}
                    </span>

                </div>

            </div>


            <div class="row-actions">

                <button
                    class="restore"
                    @click="restoreTask(task)"
                >
                    <RotateCcw :size="14" /> Restaurer
                </button>

                <button
                    class="delete"
                    :disabled="deleting === task.id"
                    @click="deleteTask(task)"
                >
                    <Trash2 :size="14" />
                    {{ deleting === task.id ? "..." : "Supprimer" }}
                </button>

            </div>

        </div>

    </div>


</div>


</template>


<style scoped>

.trash-page {

    min-height: 100vh;
    padding: 32px;
    background: transparent;
    color: white;

}


.trash-header {

    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 35px;
    flex-wrap: wrap;
    gap: 20px;

}


.trash-header h1 {

    margin: 0;
    font-size: 32px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 10px;

}


.page-icon {

    color: var(--accent);

}


.empty-icon {

    color: var(--text);
    opacity: .5;

}


.trash-header p {

    margin-top: 8px;
    color: var(--text);

}


.count {

    padding: 12px 20px;
    border-radius: 999px;
    background: var(--surface-2);
    border: 1px solid #334155;
    color: #cbd5e1;
    font-weight: 600;

}


.loading {

    height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #cbd5e1;
    font-size: 18px;

}


.empty {

    min-height: 350px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: var(--surface-2);
    border-radius: 25px;
    border: 1px solid #334155;
    text-align: center;

}


.empty span {

    font-size: 60px;

}

.empty h2 {

    margin: 15px 0 5px;

}

.empty p {

    color: var(--text);

}


.trash-list {

    display: flex;
    flex-direction: column;
    gap: 10px;

}


.trash-row {

    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 18px;
    transition: .2s;

}


.trash-row:hover {

    border-color: var(--accent-border);
    transform: translateX(4px);

}


.row-main {

    min-width: 0;
    flex: 1;

}


.row-main h3 {

    margin: 0 0 8px;
    font-size: 15px;
    font-weight: 700;
    color: var(--text-h);

}


.row-meta {

    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;

}


.status-badge {

    padding: 4px 10px;
    border-radius: 999px;
    background: var(--surface-3);
    font-size: 10px;
    font-weight: 700;
    color: var(--text-strong);
    text-transform: uppercase;

}


.meta-item {

    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    color: var(--text);
    background: var(--surface-2);
    padding: 4px 10px;
    border-radius: 8px;
    white-space: nowrap;

}


.row-actions {

    display: flex;
    gap: 8px;
    flex-shrink: 0;

}


.row-actions button {

    display: inline-flex;
    align-items: center;
    gap: 7px;
    border: none;
    padding: 10px 16px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    font-size: 13px;
    transition: .2s;
    color: white;
    white-space: nowrap;

}


.restore {

    background: #16a34a;

}

.restore:hover {

    background: #15803d;
    transform: translateY(-2px);

}


.delete {

    background: #dc2626;

}

.delete:hover {

    background: #b91c1c;
    transform: translateY(-2px);

}


.delete:disabled {

    opacity: .6;
    cursor: not-allowed;

}


@media (max-width: 700px) {

    .trash-page {

        padding: 18px;

    }

    .trash-header {

        flex-direction: column;
        align-items: flex-start;

    }

    .trash-row {

        flex-direction: column;
        align-items: stretch;

    }

    .row-actions {

        width: 100%;

    }

    .row-actions button {

        flex: 1;
        justify-content: center;
        min-height: 42px;

    }

}

</style>
