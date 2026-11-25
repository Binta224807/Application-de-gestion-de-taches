<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { spaceName } from "../services/space";
import { FolderKanban, Star, CircleCheck, Plus, X } from "lucide-vue-next";

const router = useRouter();

const projects = ref([]);
const loading = ref(true);

const COLORS = [
    "#6366f1", "#3b82f6", "#06b6d4", "#22c55e",
    "#f59e0b", "#ef4444", "#ec4899", "#8b5cf6",
];

const ICONS = ["📁", "🚀", "💼", "🎯", "📊", "🏠", "💡", "🔧", "📱", "🌐"];

const showForm = ref(false);
const saving = ref(false);
const formError = ref("");

const form = ref({
    name: "",
    description: "",
    color: COLORS[0],
    icon: ICONS[0],
});

const loadProjects = async () => {
    try {
        loading.value = true;
        const response = await api.get("projects/");
        projects.value = response.data;
    } catch (error) {
        console.error(error);
    } finally {
        loading.value = false;
    }
};

const openForm = () => {
    form.value = {
        name: "",
        description: "",
        color: COLORS[0],
        icon: ICONS[0],
    };
    formError.value = "";
    showForm.value = true;
};

const createProject = async () => {
    if (!form.value.name.trim()) {
        formError.value = "Le nom du projet est requis.";
        return;
    }

    try {
        saving.value = true;
        formError.value = "";

        await api.post("projects/", {
            name: form.value.name.trim(),
            description: form.value.description.trim(),
            color: form.value.color,
            icon: form.value.icon,
        });

        showForm.value = false;
        await loadProjects();
    } catch (error) {
        formError.value =
            error.response?.data?.name?.[0] ||
            error.response?.data?.error ||
            "Erreur lors de la création.";
    } finally {
        saving.value = false;
    }
};

const goProject = (id) => router.push(`/projects/${id}`);

onMounted(loadProjects);
</script>

<template>
<div class="projects-page">

    <header class="page-header anim-fade-up">
        <div>
            <h1>
                <FolderKanban :size="26" class="page-icon" />
                Projets
            </h1>
            <p>Progression de {{ spaceName }}</p>
        </div>

        <button class="new-project-btn" @click="openForm">
            <Plus :size="16" /> Nouveau projet
        </button>
    </header>


    <div v-if="loading" class="loading">
        <div class="loading-dots"><span></span><span></span><span></span></div>
    </div>


    <div v-else-if="projects.length" class="projects-grid stagger">

        <button
            v-for="p in projects"
            :key="p.id"
            class="project-card"
            @click="goProject(p.id)"
        >
            <div class="card-top">

                <span
                    class="project-icon"
                    :style="{ background: (p.color || '#6366f1') + '22' }"
                >
                    {{ p.icon || "📁" }}
                </span>

                <div class="project-names">
                    <strong>{{ p.name }}</strong>
                    <small>{{ p.description || "Aucune description" }}</small>
                </div>

                <Star
                    v-if="p.is_favorite"
                    :size="15"
                    class="fav-icon"
                />

            </div>

            <div class="card-progress">

                <div class="progress-info">
                    <span class="progress-count">
                        <CircleCheck :size="12" />
                        {{ p.completed_tasks }}/{{ p.total_tasks }} tâches
                    </span>
                    <span
                        class="progress-pct"
                        :style="{ color: p.color || 'var(--accent)' }"
                    >
                        {{ p.progress }}%
                    </span>
                </div>

                <div class="progress-bar">
                    <span
                        class="progress-fill"
                        :style="{
                            width: p.progress + '%',
                            background: p.color || 'var(--accent)',
                        }"
                    />
                </div>

            </div>

        </button>

    </div>


    <div v-else class="empty">
        <FolderKanban :size="44" />
        <h2>Aucun projet</h2>
        <p>Crée un projet pour regrouper tes tâches et suivre leur avancement.</p>

        <button class="new-project-btn" @click="openForm">
            <Plus :size="16" /> Nouveau projet
        </button>
    </div>


    <!-- MODALE CRÉATION -->
    <Transition name="modal">

        <div
            v-if="showForm"
            class="modal-overlay"
            @click.self="showForm = false"
        >

            <div class="project-modal anim-pop">

                <div class="modal-head">
                    <h2>Nouveau projet</h2>
                    <button class="close-btn" @click="showForm = false">
                        <X :size="17" />
                    </button>
                </div>

                <label class="field">
                    <span>Nom du projet *</span>
                    <input
                        v-model="form.name"
                        type="text"
                        placeholder="Ex : Refonte du site web"
                        maxlength="150"
                        @keyup.enter="createProject"
                    />
                </label>

                <label class="field">
                    <span>Description</span>
                    <textarea
                        v-model="form.description"
                        rows="3"
                        placeholder="Objectif du projet (optionnel)"
                    />
                </label>

                <div class="field">
                    <span>Couleur</span>
                    <div class="color-row">
                        <button
                            v-for="c in COLORS"
                            :key="c"
                            class="color-swatch"
                            :class="{ active: form.color === c }"
                            :style="{ background: c }"
                            @click="form.color = c"
                        />
                    </div>
                </div>

                <div class="field">
                    <span>Icône</span>
                    <div class="icon-row">
                        <button
                            v-for="i in ICONS"
                            :key="i"
                            class="icon-choice"
                            :class="{ active: form.icon === i }"
                            @click="form.icon = i"
                        >
                            {{ i }}
                        </button>
                    </div>
                </div>

                <p v-if="formError" class="form-error">{{ formError }}</p>

                <div class="modal-actions">
                    <button
                        class="btn-cancel"
                        @click="showForm = false"
                    >
                        Annuler
                    </button>
                    <button
                        class="btn-create"
                        :disabled="saving"
                        @click="createProject"
                    >
                        {{ saving ? "Création..." : "Créer le projet" }}
                    </button>
                </div>

            </div>

        </div>

    </Transition>

</div>
</template>

<style scoped>
.projects-page {
    min-height: 100vh;
    padding: 32px;
    background: transparent;
    color: var(--text);
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
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

/* GRILLE */

.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
}

.project-card {
    display: flex;
    flex-direction: column;
    gap: 18px;
    padding: 20px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-l);
    cursor: pointer;
    font-family: inherit;
    text-align: left;
    transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
}

.project-card:hover {
    border-color: var(--accent-border);
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
}

.card-top {
    display: flex;
    align-items: center;
    gap: 14px;
}

.project-icon {
    width: 48px;
    height: 48px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}

.project-names {
    flex: 1;
    min-width: 0;
}

.project-names strong {
    display: block;
    color: var(--text-h);
    font-size: 15px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.project-names small {
    color: var(--text);
    font-size: 12px;
    display: block;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.fav-icon {
    color: var(--warning);
    flex-shrink: 0;
}

/* PROGRESSION */

.progress-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.progress-count {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    color: var(--text);
}

.progress-pct {
    font-family: var(--display);
    font-size: 17px;
    font-weight: 700;
}

.progress-bar {
    height: 8px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
}

.progress-fill {
    display: block;
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
}

/* VIDE */

.empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 70px 30px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-l);
    color: var(--text);
    text-align: center;
}

.empty h2 {
    color: var(--text-h);
    margin: 8px 0 0;
}

.empty p {
    margin-bottom: 10px;
}

/* BOUTON NOUVEAU */

.new-project-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-family: inherit;
    font-size: 14px;
    font-weight: 700;
    color: white;
    background: var(--accent);
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
}

.new-project-btn:hover {
    background: var(--accent-strong);
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(59, 130, 246, 0.32);
}

/* MODALE */

.modal-overlay {
    position: fixed;
    inset: 0;
    z-index: 1200;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(2, 6, 23, 0.72);
    backdrop-filter: blur(6px);
}

.project-modal {
    width: 100%;
    max-width: 460px;
    background: var(--surface);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-l);
    padding: 26px;
    max-height: 90dvh;
    overflow-y: auto;
}

.modal-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.modal-head h2 {
    font-family: var(--display);
    font-size: 19px;
    color: var(--text-h);
    margin: 0;
}

.close-btn {
    width: 34px;
    height: 34px;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: var(--surface-2);
    color: var(--text);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: 0.2s;
}

.close-btn:hover {
    color: var(--text-h);
    border-color: var(--border-strong);
}

/* CHAMPS */

.field {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 16px;
}

.field > span {
    font-size: 12px;
    font-weight: 600;
    color: var(--text);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.field input,
.field textarea {
    width: 100%;
    box-sizing: border-box;
    padding: 12px 14px;
    border-radius: 11px;
    border: 1px solid var(--border);
    background: var(--surface-2);
    color: var(--text-h);
    font-family: inherit;
    font-size: 16px;
    outline: none;
    resize: vertical;
    transition: border-color 0.2s;
}

.field input:focus,
.field textarea:focus {
    border-color: var(--accent);
}

.color-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.color-swatch {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    border: 2px solid transparent;
    cursor: pointer;
    transition: transform 0.15s, border-color 0.15s;
    padding: 0;
}

.color-swatch:hover {
    transform: scale(1.12);
}

.color-swatch.active {
    border-color: white;
    box-shadow: 0 0 0 3px var(--accent-soft);
}

.icon-row {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}

.icon-choice {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--surface-2);
    font-size: 18px;
    cursor: pointer;
    transition: border-color 0.15s, transform 0.15s;
    padding: 0;
}

.icon-choice:hover {
    transform: scale(1.08);
    border-color: var(--accent-border);
}

.icon-choice.active {
    border-color: var(--accent);
    background: var(--accent-soft);
}

.form-error {
    color: var(--danger);
    font-size: 13px;
    margin: 0 0 14px;
}

.modal-actions {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
    margin-top: 22px;
}

.btn-cancel,
.btn-create {
    border-radius: 11px;
    padding: 12px 20px;
    font-family: inherit;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.2s;
}

.btn-cancel {
    border: 1px solid var(--border);
    background: transparent;
    color: var(--text);
}

.btn-cancel:hover {
    color: var(--text-h);
    border-color: var(--border-strong);
}

.btn-create {
    border: none;
    background: var(--accent);
    color: white;
}

.btn-create:hover:not(:disabled) {
    background: var(--accent-strong);
}

.btn-create:disabled {
    opacity: 0.6;
    cursor: default;
}

/* RESPONSIVE */

@media (max-width: 640px) {
    .projects-page {
        padding: 16px;
    }

    .projects-grid {
        grid-template-columns: 1fr;
    }

    .new-project-btn {
        width: 100%;
        justify-content: center;
        min-height: 46px;
    }

    .modal-overlay {
        padding: 0;
        align-items: flex-end;
    }

    .project-modal {
        max-width: none;
        border-radius: 20px 20px 0 0;
        padding-bottom: max(26px, env(safe-area-inset-bottom));
    }
}
</style>
