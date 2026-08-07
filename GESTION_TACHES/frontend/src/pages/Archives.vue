<script setup>

import { ref, onMounted } from "vue";
import api from "../services/api";


const tasks = ref([]);

const loading = ref(true);

const deleting = ref(null);



// =====================================
// CHARGER LES ARCHIVES
// =====================================

const loadArchives = async () => {

    try {

        loading.value = true;

        const response = await api.get(
            "archives/"
        );

        tasks.value = response.data;


    } catch(error){

        console.error(
            "Erreur archives :",
            error.response?.data || error
        );

    } finally {

        loading.value = false;

    }

};




// =====================================
// RESTAURER UNE TACHE
// =====================================

const restoreTask = async (task) => {


    try {


        await api.post(
            `tasks/${task.id}/restore/`
        );


        tasks.value =
            tasks.value.filter(
                item => item.id !== task.id
            );


    }

    catch(error){

        console.error(
            "Erreur restauration :",
            error.response?.data || error
        );

    }


};




// =====================================
// SUPPRIMER DEFINITIVEMENT
// =====================================

const deleteTask = async(task)=>{


    const confirmDelete =
        window.confirm(
            "Supprimer définitivement cette tâche ?"
        );


    if(!confirmDelete)
        return;



    try{


        deleting.value = task.id;


        await api.delete(
            `tasks/${task.id}/delete/`
            );

        tasks.value =
            tasks.value.filter(
                item => item.id !== task.id
            );


    }

    catch(error){

        console.error(
            "Erreur suppression :",
            error.response?.data || error
        );

    }

    finally{

        deleting.value = null;

    }


};




// =====================================
// FORMAT DATE
// =====================================

const formatDate = (date)=>{


    if(!date)
        return "Non défini";


    return new Date(date)
        .toLocaleDateString(
            "fr-FR"
        );


};





onMounted(()=>{

    loadArchives();

});


</script>



<template>


<div class="archives-page">



    <!-- HEADER -->

    <div class="archives-header">


        <div>

            <h1>
                📦 Archives
            </h1>


            <p>
                Retrouvez vos tâches archivées.
            </p>


        </div>


        <div class="count">

            {{ tasks.length }}
            tâche(s)

        </div>


    </div>





    <!-- LOADING -->

    <div
        v-if="loading"
        class="loading"
    >

        Chargement des archives...

    </div>





    <!-- VIDE -->

    <div
        v-else-if="!tasks.length"
        class="empty"
    >

        <span>
            📂
        </span>

        <h2>
            Aucune tâche archivée
        </h2>

        <p>
            Les tâches archivées apparaîtront ici.
        </p>


    </div>





    <!-- LISTE -->

    <div
        v-else
        class="archives-grid"
    >



        <div

            v-for="task in tasks"

            :key="task.id"

            class="archive-card"

        >



            <div class="card-top">


                <h3>
                    {{ task.title }}
                </h3>


                <span
                    class="status"
                >

                    {{ task.status }}

                </span>



            </div>





            <p class="description">

                {{ task.description || "Aucune description" }}

            </p>





            <div class="infos">


                <span>

                    📁

                    {{ task.project_name || "Sans projet" }}

                </span>



                <span>

                    🏷️

                    {{ task.category_name || "Sans catégorie" }}

                </span>



                <span>

                    📅

                    Archivée le :

                    {{ formatDate(task.archived_at) }}

                </span>



                <span>

                    ⏳

                    {{ task.archive_duration || "Permanent" }}

                </span>



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

                    🗑

                    {{
                        deleting === task.id
                        ? "Suppression..."
                        : "Supprimer"
                    }}

                </button>



            </div>



        </div>



    </div>



</div>



</template>

<style scoped>


.archives-page{

    min-height:100vh;

    padding:32px;

    background:#0f172a;

    color:white;

}



/* ===============================
   HEADER
================================ */


.archives-header{

    display:flex;

    justify-content:space-between;

    align-items:center;

    margin-bottom:35px;

}


.archives-header h1{

    margin:0;

    font-size:32px;

    font-weight:800;

}


.archives-header p{

    margin-top:8px;

    color:#94a3b8;

}



.count{

    padding:12px 20px;

    border-radius:999px;

    background:#1e293b;

    border:1px solid #334155;

    color:#cbd5e1;

    font-weight:600;

}



/* ===============================
   LOADING
================================ */


.loading{

    height:400px;

    display:flex;

    justify-content:center;

    align-items:center;

    color:#cbd5e1;

    font-size:18px;

}



/* ===============================
   EMPTY
================================ */


.empty{

    min-height:350px;

    display:flex;

    flex-direction:column;

    justify-content:center;

    align-items:center;

    background:#1e293b;

    border-radius:25px;

    border:1px solid #334155;

    text-align:center;

}



.empty span{

    font-size:60px;

}



.empty h2{

    margin:15px 0 5px;

}



.empty p{

    color:#94a3b8;

}



/* ===============================
   GRID
================================ */


.archives-grid{

    display:grid;

    grid-template-columns:
    repeat(auto-fit,minmax(320px,1fr));

    gap:25px;

}



/* ===============================
   CARD
================================ */


.archive-card{

    background:#1e293b;

    border:1px solid #334155;

    border-radius:24px;

    padding:24px;

    display:flex;

    flex-direction:column;

    gap:18px;

    transition:.25s;

}



.archive-card:hover{

    transform:translateY(-5px);

    box-shadow:
    0 20px 40px rgba(0,0,0,.35);

}



/* ===============================
   TOP
================================ */


.card-top{

    display:flex;

    justify-content:space-between;

    align-items:flex-start;

    gap:15px;

}



.card-top h3{

    margin:0;

    font-size:20px;

    font-weight:750;

}



.status{

    padding:6px 12px;

    border-radius:999px;

    background:#334155;

    font-size:12px;

    color:#cbd5e1;

}



/* ===============================
   DESCRIPTION
================================ */


.description{

    color:#94a3b8;

    line-height:1.6;

    font-size:14px;

}



/* ===============================
   INFOS
================================ */


.infos{

    display:flex;

    flex-direction:column;

    gap:10px;

    color:#cbd5e1;

    font-size:14px;

}



.infos span{

    background:#0f172a;

    padding:10px 14px;

    border-radius:12px;

}



/* ===============================
   ACTIONS
================================ */


.actions{

    display:flex;

    gap:12px;

    margin-top:auto;

}



.actions button{

    flex:1;

    border:none;

    padding:13px;

    border-radius:14px;

    cursor:pointer;

    font-weight:700;

    transition:.25s;

    color:white;

}



/* RESTAURER */


.restore{

    background:#16a34a;

}


.restore:hover{

    background:#15803d;

    transform:translateY(-2px);

}



/* SUPPRIMER */


.delete{

    background:#dc2626;

}



.delete:hover{

    background:#b91c1c;

    transform:translateY(-2px);

}



.delete:disabled{

    opacity:.6;

    cursor:not-allowed;

}



/* ===============================
   RESPONSIVE
================================ */


@media(max-width:700px){


    .archives-page{

        padding:18px;

    }


    .archives-header{

        flex-direction:column;

        align-items:flex-start;

        gap:20px;

    }


    .actions{

        flex-direction:column;

    }


}


</style>