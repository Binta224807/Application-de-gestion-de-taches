<template>

<div class="detail-page">

    <!-- LOADING -->

    <div
        v-if="loading"
        class="loading"
    >
        Chargement...
    </div>


    <!-- ERREUR -->

    <div
        v-else-if="error"
        class="error-state"
    >
        {{ error }}
    </div>


    <!-- CONTENU -->

    <template v-else-if="task">

        <!-- HEADER -->

        <div class="detail-header">

            <div>

                <button
                    class="back-btn"
                    @click="goBack"
                >
                    ← Retour
                </button>

                <h1 class="detail-title">
                    {{ task.title }}
                </h1>

                <div class="badges">

                    <span
                        class="badge status"
                        :class="task.status"
                    >
                        {{ statusLabel }}
                    </span>

                    <span
                        class="badge priority"
                        :class="task.priority"
                    >
                        {{ priorityLabel }}
                    </span>

                </div>

            </div>


            <div class="header-actions">

                <button
                    v-if="canEdit"
                    class="btn-edit"
                    @click="openEditForm"
                >
                    <Pencil :size="15" /> Modifier
                </button>

                <button
                    v-if="canDelete"
                    class="btn-delete"
                    @click="deleteTask"
                >
                    <Trash2 :size="15" /> Supprimer
                </button>

            </div>

        </div>


        <!-- INFORMATIONS -->

        <div class="detail-grid">

            <div class="detail-card main-info">

                <h2><FileText :size="18" class="section-icon" /> Description</h2>

                <p class="description">
                    {{ task.description || "Aucune description" }}
                </p>

            </div>


            <div class="detail-card meta-info">

                <h2><ClipboardList :size="18" class="section-icon" /> Informations</h2>

                <div class="meta-list">

                    <div class="meta-item">
                        <span class="meta-label">Employé assigné</span>
                        <span class="meta-value">
                            {{ assignedName }}
                        </span>
                    </div>

                    <div class="meta-item">
                        <span class="meta-label">Créée par</span>
                        <span class="meta-value">
                            {{ task.created_by || "Inconnu" }}
                        </span>
                    </div>

                    <div class="meta-item">
                        <span class="meta-label">Priorité</span>
                        <span class="meta-value">
                            {{ priorityLabel }}
                        </span>
                    </div>

                    <div class="meta-item">
                        <span class="meta-label">Durée estimée</span>
                        <span class="meta-value">
                            {{ formatDuration(task.estimated_duration) }}
                        </span>
                    </div>

                    <div class="meta-item">
                        <span class="meta-label">Échéance</span>
                        <span class="meta-value">
                            {{ task.due_date || "Non définie" }}
                            <span v-if="task.due_time"> à {{ task.due_time }}</span>
                        </span>
                    </div>

                    <div class="meta-item">
                        <span class="meta-label">Date de création</span>
                        <span class="meta-value">
                            {{ formatDate(task.created_at) }}
                        </span>
                    </div>

                </div>

            </div>


            <!-- ACTIONS DE STATUT -->

            <div class="detail-card status-actions">

                <h2>🔄 Changement de statut</h2>

                <div class="status-buttons">

                    <button
                        v-if="task.status !== 'todo'"
                        class="btn-status todo"
                        @click="changeStatus('todo')"
                    >
                        À faire
                    </button>

                    <button
                        v-if="task.status !== 'in_progress'"
                        class="btn-status in_progress"
                        @click="changeStatus('in_progress')"
                    >
                        En cours
                    </button>

                    <button
                        v-if="task.status !== 'done'"
                        class="btn-status done"
                        @click="changeStatus('done')"
                    >
                        Terminée
                    </button>

                </div>

            </div>

        </div>


        <Transition name="modal">

        <TaskForm
            v-if="showTaskForm"
            :task="task"
            @close="closeEditForm"
            @saved="reloadTask"
        />

    </Transition>

    </template>

</div>

</template>

<script setup>

import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import { formatDuration } from "../services/formatDuration.js";
import TaskForm from "../components/TaskForm.vue";
import { Pencil, Trash2, FileText, ClipboardList } from "lucide-vue-next";


const route = useRoute();
const router = useRouter();

const task = ref(null);
const loading = ref(true);
const error = ref("");
const showTaskForm = ref(false);

import { isAdmin } from "../services/space";
const isCEO = isAdmin;
const currentUser = ref(localStorage.getItem("username"));


const statusLabel = computed(() => {

    const labels = {
        todo: "À faire",
        in_progress: "En cours",
        review: "À vérifier",
        done: "Terminée",
    };

    return labels[task.value?.status] || task.value?.status;

});


const priorityLabel = computed(() => {

    const labels = {
        low: "Faible",
        medium: "Moyenne",
        high: "Élevée",
        urgent: "Urgente",
    };

    return labels[task.value?.priority] || task.value?.priority;

});


const assignedName = computed(() => {

    const assignees = task.value?.assigned_to || [];

    if (!assignees.length) {

        return "Non assigné";

    }

    return assignees
        .map((u) => u.username)
        .join(", ");

});


const canEdit = computed(() => {

    if (isCEO.value) return true;

    const assignees = task.value?.assigned_to || [];

    return assignees.some(
        (u) => u.username === currentUser.value
    );

});


const canDelete = computed(() => {

    if (isCEO.value) return true;

    const assignees = task.value?.assigned_to || [];

    return assignees.some(
        (u) => u.username === currentUser.value
    );

});


const loadTask = async () => {

    try {

        loading.value = true;

        const response = await api.get(`tasks/${route.params.id}/`);

        task.value = response.data;

    }

    catch (err) {

        console.error(err);
        error.value = "Tâche introuvable.";

    }

    finally {

        loading.value = false;

    }

};


const reloadTask = async () => {

    await loadTask();

};


const goBack = () => {

    router.push("/tasks");

};


const openEditForm = () => {

    showTaskForm.value = true;

};


const closeEditForm = () => {

    showTaskForm.value = false;

};


const changeStatus = async (newStatus) => {

    try {

        await api.patch(`tasks/${task.value.id}/`, {
            status: newStatus,
        });

        await loadTask();

    }

    catch (err) {

        console.error("Erreur changement de statut :", err);
        alert("Impossible de changer le statut.");

    }

};


const deleteTask = async () => {

    const confirmation = confirm("Déplacer cette tâche dans la corbeille ?");

    if (!confirmation) return;

    try {

        await api.delete(`tasks/${task.value.id}/`);

        router.push("/tasks");

    }

    catch (err) {

        console.error("Erreur suppression :", err);
        alert("Impossible de supprimer la tâche.");

    }

};


const formatDate = (dateString) => {

    if (!dateString) return "Non définie";

    return new Date(dateString).toLocaleDateString("fr-FR", {
        day: "2-digit",
        month: "long",
        year: "numeric",
    });

};


onMounted(() => {

    loadTask();

});


</script>

<style scoped>

.detail-page {

    padding: 32px;
    min-height: 100vh;
    background: transparent;
    color: white;

}


.loading,
.error-state {

    color: var(--text);
    text-align: center;
    padding: 60px;

}


.error-state {

    color: #ef4444;

}


.detail-header {

    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
    flex-wrap: wrap;
    gap: 20px;

}


.back-btn {

    background: transparent;
    color: var(--text);
    border: none;
    padding: 0;
    margin-bottom: 12px;
    cursor: pointer;
    font-size: 14px;
    transition: .2s;

}


.back-btn:hover {

    color: white;

}


.detail-title {

    font-size: 32px;
    font-weight: 800;
    color: white;
    margin: 0 0 12px 0;

}


.badges {

    display: flex;
    gap: 10px;
    flex-wrap: wrap;

}


.badge {

    padding: 6px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    color: white;

}


.priority.low {
    background: #22c55e;
}

.priority.medium {
    background: #f59e0b;
}

.priority.high {
    background: #ef4444;
}

.priority.urgent {
    background: #dc2626;
}


.status.todo {
    background: var(--accent);
}

.status.in_progress {
    background: #d97706;
}

.status.review {
    background: #8b5cf6;
}

.status.done {
    background: #16a34a;
}


.header-actions {

    display: flex;
    gap: 12px;
    flex-wrap: wrap;

}


.btn-edit,
.btn-delete {

    padding: 12px 20px;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    font-size: 14px;
    transition: .2s;

}


.btn-edit {

    background: var(--accent-strong);
    color: white;

}


.btn-edit:hover {

    background: var(--accent-strong);

}


.btn-delete {

    background: #dc2626;
    color: white;

}


.btn-delete:hover {

    background: #b91c1c;

}


.detail-grid {

    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 24px;

}


.detail-card {

    background: var(--surface);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 24px;

}


.detail-card h2 {

    font-size: 18px;
    font-weight: 700;
    margin: 0 0 16px 0;
    color: white;

}


.description {

    color: #cbd5e1;
    line-height: 1.7;
    margin: 0;
    white-space: pre-wrap;

}


.meta-list {

    display: flex;
    flex-direction: column;
    gap: 14px;

}


.meta-item {

    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);

}


.meta-item:last-child {

    border-bottom: none;
    padding-bottom: 0;

}


.meta-label {

    color: var(--text);
    font-size: 14px;

}


.meta-value {

    color: white;
    font-weight: 600;
    font-size: 14px;
    text-align: right;

}


.status-actions {

    grid-column: 1 / -1;

}


.status-buttons {

    display: flex;
    gap: 12px;
    flex-wrap: wrap;

}


.btn-status {

    padding: 12px 24px;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    color: white;
    transition: .2s;
    font-size: 14px;

}


.btn-status:hover {

    transform: translateY(-2px);
    opacity: 0.9;

}


.btn-status.todo {
    background: var(--accent);
}

.btn-status.in_progress {
    background: #d97706;
}

.btn-status.done {
    background: #16a34a;
}


@media (max-width: 1024px) {

    .detail-grid {

        grid-template-columns: 1fr;

    }

}


@media (max-width: 768px) {

    .detail-page {

        padding: 18px;

    }

    .detail-header {

        flex-direction: column;

    }

    .detail-title {

        font-size: 26px;

    }

    .header-actions {

        width: 100%;

    }

    .btn-edit,
    .btn-delete {

        flex: 1;

    }

    .meta-item {

        flex-direction: column;
        align-items: flex-start;
        gap: 4px;

    }

    .meta-value {

        text-align: left;

    }

    .status-buttons {

        flex-direction: column;

    }

    .btn-status {

        width: 100%;

    }

}

</style>
