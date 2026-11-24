<script setup>
import { Hourglass } from "lucide-vue-next";

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
            <h1>�️ Corbeille</h1>
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

        <span>�️</span>
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
            class="trash-card"
        >

            <div class="card-top">

                <h3>{{ task.title }}</h3>

                <span class="status-badge">
                    {{ task.status }}
                </span>

            </div>


            <p class="description">
                {{ task.description || "Aucune description" }}
            </p>


            <div class="infos">

                <span>� Assignée à : {{ assignedName(task) }}</span>

                <span class="meta"><Hourglass :size="14" /> Durée : {{ formatDuration(task.estimated_duration) }}</span>

                <span>�️ Supprimée le : {{ formatDate(task.deleted_at) }}</span>

            </div>


            <div class="actions">

                <button
                    class="restore"
                    @click="restoreTask(task)"
                >
                    ♻ Restaurer
                </button>

                <button
                    class="delete"
                    :disabled="deleting === task.id"
                    @click="deleteTask(task)"
                >
                    {{
                        deleting === task.id
                        ? "Suppression..."
                        : "Supprimer définitivement"
                    }}
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
    background: #0f172a;
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

}


.trash-header p {

    margin-top: 8px;
    color: #94a3b8;

}


.count {

    padding: 12px 20px;
    border-radius: 999px;
    background: #1e293b;
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
    background: #1e293b;
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

    color: #94a3b8;

}


.trash-list {

    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 25px;

}


.trash-card {

    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 24px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 18px;
    transition: .25s;

}


.trash-card:hover {

    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, .35);

}


.card-top {

    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 15px;

}


.card-top h3 {

    margin: 0;
    font-size: 20px;
    font-weight: 750;

}


.status-badge {

    padding: 6px 12px;
    border-radius: 999px;
    background: #334155;
    font-size: 12px;
    color: #cbd5e1;
    text-transform: uppercase;

}


.description {

    color: #94a3b8;
    line-height: 1.6;
    font-size: 14px;

}


.infos {

    display: flex;
    flex-direction: column;
    gap: 10px;
    color: #cbd5e1;
    font-size: 14px;

}


.infos span {

    background: #0f172a;
    padding: 10px 14px;
    border-radius: 12px;

}


.actions {

    display: flex;
    gap: 12px;
    margin-top: auto;

}


.actions button {

    flex: 1;
    border: none;
    padding: 13px;
    border-radius: 14px;
    cursor: pointer;
    font-weight: 700;
    transition: .25s;
    color: white;

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

    .actions {

        flex-direction: column;

    }

}

</style>
