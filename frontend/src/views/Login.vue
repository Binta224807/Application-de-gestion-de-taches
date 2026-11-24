<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-950 p-4">
    <div
      class="w-full max-w-md bg-slate-900 p-8 rounded-3xl border border-slate-700 shadow-xl"
    >
      <div class="brand">
        <span class="brand-name">NOVA TASKS</span>
        <span class="brand-sub">Pilotage d'entreprise · by Clever</span>
      </div>

      <h1 class="text-3xl font-bold text-white text-center mb-8">
        Connexion
      </h1>

      <form
        @submit.prevent="login"
        class="space-y-5"
      >
        <input
          v-model="form.username"
          type="text"
          placeholder="Nom utilisateur"
          class="input"
          required
        />

        <input
          v-model="form.password"
          type="password"
          placeholder="Mot de passe"
          class="input"
          required
        />

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white py-3 rounded-xl font-semibold transition"
        >
          {{ loading ? "Connexion..." : "Se connecter" }}
        </button>
      </form>

      <p
        v-if="error"
        class="text-red-400 text-center mt-4"
      >
        {{ error }}
      </p>

      <p class="text-slate-400 text-center mt-6">
        Pas encore de compte ?

        <router-link
          to="/register"
          class="text-indigo-400 hover:text-indigo-300"
        >
          Créer un compte
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const loading = ref(false);
const error = ref("");

const form = reactive({
  username: "",
  password: "",
});

const login = async () => {
  error.value = "";

  if (!form.username || !form.password) {
    error.value = "Veuillez remplir tous les champs.";
    return;
  }

  try {
    loading.value = true;

    const response = await api.post("auth/login/", {
      username: form.username,
      password: form.password,
    });

    const accessToken = response.data.access;
    const refreshToken = response.data.refresh;

    if (!accessToken || !refreshToken) {
      throw new Error("Tokens JWT manquants dans la réponse.");
    }

    localStorage.setItem("access", accessToken);
    localStorage.setItem("refresh", refreshToken);
    localStorage.setItem("username", form.username);

    // Récupérer les informations de l'utilisateur via le dashboard
    const dashboardResponse = await api.get("dashboard/");
    const dashboardData = dashboardResponse.data;

    localStorage.setItem("is_ceo", dashboardData.is_ceo ? "1" : "0");

    if (dashboardData.company) {
      localStorage.setItem("company_id", String(dashboardData.company.id));
      localStorage.setItem("company_name", dashboardData.company.name);
    }

    router.push("/dashboard");

  } catch (err) {
    console.error("Erreur de connexion :", err);

    if (err.response?.data?.detail) {
      error.value = err.response.data.detail;
    } else {
      error.value = "Nom utilisateur ou mot de passe incorrect.";
    }

  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.brand {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  margin-bottom: 28px;
}

.brand-name {
  font-family: "Space Grotesk", "Inter", sans-serif;
  color: white;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 3px;
}

.brand-sub {
  color: #64748b;
  font-size: 12px;
  letter-spacing: 0.5px;
}

.input {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  background: #1e293b;
  border: 1px solid #334155;
  color: white;
  outline: none;
  transition: 0.3s;
  box-sizing: border-box;
  font-size: 15px;
}

.input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.input::placeholder {
  color: #94a3b8;
}
</style>
