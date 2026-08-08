<template>

<div class="dashboard">


    <!-- ============================= -->
    <!-- HEADER -->
    <!-- ============================= -->

    <div class="dashboard-header">

        <div>

            <h1 class="dashboard-title">
                Tableau de bord
            </h1>

            <p class="dashboard-subtitle">
                Suivez votre productivité et l'avancement de vos projets.
            </p>

        </div>

    </div>



    <!-- ============================= -->
    <!-- LOADING -->
    <!-- ============================= -->

    <div
        v-if="loading"
        class="loading-container"
    >

        Chargement des données...

    </div>



    <!-- ============================= -->
    <!-- DASHBOARD CONTENT -->
    <!-- ============================= -->

    <template v-else>



        <!-- ========================= -->
        <!-- STATISTIQUES -->
        <!-- ========================= -->


        <div class="stats-grid">


            <StatCard
                title="Total des tâches"
                icon="📋"
                :value="dashboard.total_tasks"
            />


            <StatCard
                title="À faire"
                icon="📝"
                :value="dashboard.todo_tasks"
            />


            <StatCard
                title="En cours"
                icon="⏳"
                :value="dashboard.in_progress_tasks"
            />


            <StatCard
                title="Terminées"
                icon="✅"
                :value="dashboard.done_tasks"
            />


            <StatCard
                title="Archivées"
                icon="📦"
                :value="dashboard.archived_tasks"
            />


            <StatCard
                title="Projets"
                icon="📁"
                :value="dashboard.total_projects"
            />


            <StatCard
                title="Progression globale"
                icon="📈"
                :value="dashboard.total_progress + '%'"
            />


            <StatCard
                title="Progression moyenne"
                icon="🎯"
                :value="dashboard.average_progress + '%'"
            />


        </div>




        <!-- ========================= -->
        <!-- PROGRESSION PROJETS -->
        <!-- ========================= -->


        <section class="dashboard-section">


            <h2>
                📊 Progression des projets
            </h2>



            <div
                v-if="projects.length"
                class="projects-progress"
            >


                <div

                    v-for="project in projects"

                    :key="project.id"

                    class="project-progress-card"

                >


                    <div class="project-header">


                        <span>
                            {{ project.name }}
                        </span>


                        <span>
                            {{ project.progress }}%
                        </span>


                    </div>



                    <div class="progress-bar">


                        <div

                            class="progress-fill"

                            :style="{
                                width: project.progress + '%'
                            }"

                        ></div>


                    </div>



                    <small>

                        {{ project.completed_tasks }}

                        /

                        {{ project.total_tasks }}

                        tâches terminées

                    </small>


                </div>


            </div>


            <p v-else>
                Aucun projet disponible.
            </p>


        </section>




        <!-- ========================= -->
        <!-- COLONNES INFORMATIONS -->
        <!-- ========================= -->


        <div class="dashboard-columns">


            <div class="column">


                <section class="dashboard-section">


                    <h2>
                        🔥 Tâches urgentes
                    </h2>


                    <ActivityList

                        :tasks="urgentTasks"

                    />


                </section>




                <section class="dashboard-section">


                    <h2>
                        ⚠️ Tâches en retard
                    </h2>


                    <ActivityList

                        :tasks="overdueTasks"

                    />


                </section>


            </div>

<div class="column">

            </div>


        </div>


    </template>


</div>

</template>



<script setup>

import { ref, onMounted } from "vue";

import api from "../services/api";


import StatCard from "../components/StatCard.vue";
import ActivityList from "../components/ActivityList.vue";




const loading = ref(true);



const dashboard = ref({

    total_tasks: 0,

    todo_tasks: 0,

    in_progress_tasks: 0,

    review_tasks: 0,

    done_tasks: 0,

    archived_tasks: 0,

    total_projects: 0,

    total_progress: 0,

    average_progress: 0,

});



const projects = ref([]);

const urgentTasks = ref([]);

const overdueTasks = ref([]);

const upcomingTasks = ref([]);

const goals = ref([]);





const loadDashboard = async () => {

    try {

        const response = await api.get(
            "dashboard/"
        );


        const data = response.data;



        dashboard.value = {

            ...dashboard.value,

            ...data.stats,

        };



        projects.value =
            data.projects_progress || [];



        goals.value =
            data.goals || [];



        upcomingTasks.value =
            data.deadlines || [];



    }

    catch(error){

        console.error(
            "Erreur Dashboard :",
            error.response?.data || error
        );

    }

};





const loadUrgentTasks = async () => {

    try {

        const response = await api.get(
            "tasks/?priority=urgent"
        );


        urgentTasks.value =
            response.data;


    }

    catch(error){

        console.error(error);

    }

};





const loadOverdueTasks = async () => {

    try {


        const response = await api.get(
            "tasks/?overdue=true"
        );


        overdueTasks.value =
            response.data;


    }

    catch(error){

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





onMounted(() => {

    loadDashboardData();

});


</script>




<style scoped>


.dashboard{

    padding:32px;

    min-height:100vh;

    background:#0f172a;

    display:flex;

    flex-direction:column;

    gap:32px;

}



.dashboard-header{

    display:flex;

    justify-content:space-between;

    align-items:center;

}



.dashboard-title{

    color:white;

    font-size:32px;

    font-weight:800;

}



.dashboard-subtitle{

    color:#94a3b8;

    margin-top:8px;

}




.stats-grid{

    display:grid;

    grid-template-columns:
    repeat(auto-fit,minmax(220px,1fr));

    gap:20px;

}




.dashboard-section{

    background:#1e293b;

    border:1px solid #334155;

    border-radius:20px;

    padding:24px;

}



.dashboard-section h2{

    color:white;

    margin-bottom:20px;

}




.projects-progress{

    display:flex;

    flex-direction:column;

    gap:18px;

}




.project-progress-card{

    background:#0f172a;

    padding:18px;

    border-radius:16px;

}




.project-header,

.goal-header{

    display:flex;

    justify-content:space-between;

    color:white;

    font-weight:600;

    margin-bottom:12px;

}




.progress-bar{

    height:10px;

    background:#334155;

    border-radius:20px;

    overflow:hidden;

    margin-bottom:10px;

}



.progress-fill{

    height:100%;

    background:#2563eb;

}




.dashboard-columns{

    display:grid;

    grid-template-columns:1fr 1fr;

    gap:24px;

}



.column{

    display:flex;

    flex-direction:column;

    gap:24px;

}




.goal-card{

    background:#0f172a;

    border-radius:16px;

    padding:18px;

    margin-bottom:15px;

}




.loading-container{

    color:white;

    text-align:center;

    padding:50px;

}




@media (max-width: 768px) {

    .dashboard {

        width: 100%;

        min-height: calc(100vh - 64px);

        padding: 18px 14px;

        gap: 20px;

        box-sizing: border-box;

    }


    .dashboard-header {

        width: 100%;

    }


    .dashboard-title {

        font-size: 26px;

    }


    .dashboard-subtitle {

        font-size: 14px;

        line-height: 1.5;

    }


    .stats-grid {

        width: 100%;

        grid-template-columns: 1fr !important;

        gap: 12px;

    }


    .dashboard-section {

        width: 100%;

        padding: 16px;

        border-radius: 16px;

        box-sizing: border-box;

    }


    .dashboard-section h2 {

        font-size: 18px;

    }


    .project-progress-card {

        padding: 14px;

    }


    .dashboard-columns {

        width: 100%;

        grid-template-columns: 1fr;

        gap: 16px;

    }

}

</style>            