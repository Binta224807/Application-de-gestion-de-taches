<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { spaceName } from "../services/space";
import { FolderKanban, Star, CircleCheck } from "lucide-vue-next";

const router = useRouter();

const projects = ref([]);
const loading = ref(true);

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

const goProject = (id) => router.push(`/projects/${id}`);

onMounted(loadProjects);
</script>

<template>
<div class="projects-page">

    <header class="page-header anim-fade-up">
        <h1>
            <FolderKanban :size="26" class="page-icon" />
            Projets
        </h1>
        <p>Progression de {{ spaceName }}</p>
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
        <p>Crée un projet depuis le formulaire de tâche pour regrouper tes tâches.</p>
    </div>

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

/* RESPONSIVE */

@media (max-width: 640px) {
    .projects-page {
        padding: 16px;
    }

    .projects-grid {
        grid-template-columns: 1fr;
    }
}
</style>
