<template>

<div class="company-page">

    <!-- HEADER -->

    <div class="company-header">

        <div>
            <h1><Building2 :size="26" class="page-icon" /> Mon entreprise</h1>
            <p>Gérez votre entreprise et vos employés.</p>
        </div>

    </div>


    <!-- LOADING -->

    <div
        v-if="loading"
        class="loading"
    >
        Chargement...
    </div>


    <template v-else>

        <!-- INFOS ENTREPRISE -->

        <section class="company-card">

            <h2>Informations</h2>

            <div class="info-grid">

                <div>
                    <span class="label">Nom</span>
                    <span class="value">{{ company.name }}</span>
                </div>

                <div>
                    <span class="label">Description</span>
                    <span class="value">{{ company.description || "Aucune description" }}</span>
                </div>

                <div>
                    <span class="label">PDG</span>
                    <span class="value">{{ company.owner_name }}</span>
                </div>

                <div>
                    <span class="label">Nombre d'employés</span>
                    <span class="value">{{ employees.length }}</span>
                </div>

            </div>

        </section>


        <!-- LISTE DES EMPLOYÉS -->

        <section class="company-card">

            <h2>Employés</h2>

            <div
                v-if="employees.length === 0"
                class="empty"
            >
                Aucun employé dans votre entreprise.
            </div>

            <div
                v-else
                class="employees-list"
            >

                <div
                    v-for="employee in employees"
                    :key="employee.id"
                    class="employee-card"
                >

                    <div class="employee-avatar">
                        {{ employee.username.charAt(0).toUpperCase() }}
                    </div>

                    <div class="employee-info">
                        <p class="employee-name">{{ employee.username }}</p>
                        <p class="employee-email">{{ employee.email || "Email non renseigné" }}</p>
                    </div>

                </div>

            </div>

        </section>


        <!-- AJOUTER UN EMPLOYÉ -->

        <section class="company-card invite-card">

            <h2><UserPlus :size="19" class="section-icon" /> Nouvel employé</h2>

            <p class="invite-help">
                Créez un compte employé en remplissant le formulaire ci-dessous. L'employé devra utiliser l'ID de l'entreprise : <strong>{{ company.id }}</strong>
            </p>

            <form
                @submit.prevent="createEmployee"
                class="invite-form"
            >

                <input
                    v-model="newEmployee.username"
                    type="text"
                    placeholder="Nom d'utilisateur"
                    class="input"
                    required
                />

                <input
                    v-model="newEmployee.email"
                    type="email"
                    placeholder="Email"
                    class="input"
                />

                <input
                    v-model="newEmployee.password"
                    type="password"
                    placeholder="Mot de passe"
                    class="input"
                    required
                />

                <input
                    v-model="newEmployee.password_confirmation"
                    type="password"
                    placeholder="Confirmer le mot de passe"
                    class="input"
                />

                <button
                    type="submit"
                    :disabled="creating"
                    class="btn-create"
                >
                    {{ creating ? "Création..." : "Créer l'employé" }}
                </button>

            </form>

            <p
                v-if="message"
                class="message success"
            >
                {{ message }}
            </p>

            <p
                v-if="error"
                class="message error"
            >
                {{ error }}
            </p>

        </section>

    </template>


</div>

</template>


<script setup>
import { Building2, UserPlus } from "lucide-vue-next";

import { ref, reactive, onMounted } from "vue";
import api from "../services/api";

const loading = ref(true);
const creating = ref(false);
const company = ref({});
const employees = ref([]);

const message = ref("");
const error = ref("");

const newEmployee = reactive({
    username: "",
    email: "",
    password: "",
    password_confirmation: "",
});


const loadCompany = async () => {

    try {

        const response = await api.get("companies/");

        company.value = response.data[0] || {};

    }

    catch (err) {

        console.error("Erreur entreprise :", err);

    }

};


const loadEmployees = async () => {

    try {

        const response = await api.get("employees/");

        employees.value = response.data;

    }

    catch (err) {

        console.error("Erreur employés :", err);

    }

};


const createEmployee = async () => {

    message.value = "";
    error.value = "";

    if (newEmployee.password_confirmation && newEmployee.password !== newEmployee.password_confirmation) {
        error.value = "Les mots de passe ne correspondent pas.";
        return;
    }

    try {

        creating.value = true;

        await api.post("auth/register/", {
            username: newEmployee.username,
            email: newEmployee.email,
            password: newEmployee.password,
            password_confirmation: newEmployee.password_confirmation,
            role: "employee",
            company_id: company.value.id,
        });

        message.value = "Employé créé avec succès.";

        newEmployee.username = "";
        newEmployee.email = "";
        newEmployee.password = "";
        newEmployee.password_confirmation = "";

        await loadEmployees();

    }

    catch (err) {

        error.value = err.response?.data?.error || "Erreur lors de la création de l'employé.";

    }

    finally {

        creating.value = false;

    }

};


onMounted(async () => {

    await Promise.all([
        loadCompany(),
        loadEmployees(),
    ]);

    loading.value = false;

});


</script>


<style scoped>

.company-page {

    padding: 32px;
    min-height: 100vh;
    background: transparent;
    color: white;

}


.company-header {

    margin-bottom: 32px;

}


.company-header h1 {

    font-size: 32px;
    font-weight: 800;
    margin: 0 0 8px 0;

}


.company-header p {

    color: #94a3b8;

}


.loading {

    color: #94a3b8;
    text-align: center;
    padding: 60px;

}


.company-card {

    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 24px;

}


.company-card h2 {

    font-size: 18px;
    font-weight: 700;
    margin: 0 0 20px 0;

}


.info-grid {

    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;

}


.info-grid > div {

    display: flex;
    flex-direction: column;
    gap: 6px;

}


.label {

    color: #94a3b8;
    font-size: 13px;

}


.value {

    color: white;
    font-weight: 600;
    font-size: 15px;

}


.employees-list {

    display: flex;
    flex-direction: column;
    gap: 12px;

}


.employee-card {

    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;
    background: #0f172a;
    border-radius: 14px;

}


.employee-avatar {

    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2563eb, #9333ea);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;

}


.employee-name {

    font-weight: 600;
    color: white;
    margin: 0 0 2px 0;

}


.employee-email {

    color: #94a3b8;
    font-size: 13px;
    margin: 0;

}


.empty {

    color: #94a3b8;
    padding: 20px 0;

}


.invite-help {

    color: #cbd5e1;
    line-height: 1.6;
    margin-bottom: 20px;

}


.invite-form {

    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    align-items: end;

}


.input {

    width: 100%;
    padding: 12px 16px;
    border-radius: 12px;
    background: #1e293b;
    border: 1px solid #334155;
    color: white;
    outline: none;
    box-sizing: border-box;
    font-size: 15px;

}


.input:focus {

    border-color: #2563eb;

}


.btn-create {

    background: #2563eb;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 600;
    cursor: pointer;
    transition: .2s;

}


.btn-create:hover {

    background: #1d4ed8;

}


.btn-create:disabled {

    opacity: 0.6;
    cursor: not-allowed;

}


.message {

    margin-top: 16px;
    font-size: 14px;

}


.success {

    color: #22c55e;

}


.error {

    color: #ef4444;

}


@media (max-width: 768px) {

    .company-page {

        padding: 18px;

    }

    .company-header h1 {

        font-size: 26px;

    }

    .invite-form {

        grid-template-columns: 1fr;

    }

    .btn-create {

        width: 100%;

    }

}

</style>
