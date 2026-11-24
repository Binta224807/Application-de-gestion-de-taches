<template>
  <div class="auth-page min-h-screen flex items-center justify-center bg-slate-950 p-4">
        <Starfield />
    <div class="auth-glow glow-a"></div>
    <div class="auth-glow glow-b"></div>
    <div
      class="w-full max-w-md bg-slate-900 rounded-3xl p-8 shadow-2xl border border-slate-700"
    >
      <h1 class="text-3xl font-bold text-white text-center mb-6">
        Créer un compte
      </h1>

      <form
        @submit.prevent="register"
        class="space-y-4"
      >
        <input
          v-model="form.username"
          type="text"
          placeholder="Nom utilisateur"
          class="input"
          required
        />

        <input
          v-model="form.email"
          type="email"
          placeholder="Email"
          class="input"
        />

        <input
          v-model="form.password"
          type="password"
          placeholder="Mot de passe"
          class="input"
          required
        />

        <input
          v-model="form.password_confirmation"
          type="password"
          placeholder="Confirmer le mot de passe"
          class="input"
        />

        <select
          v-model="form.role"
          class="input"
        >
          <option value="ceo">
            PDG / Administrateur
          </option>

          <option value="employee">
            Employé
          </option>
        </select>

        <div
          v-if="form.role === 'ceo'"
          class="space-y-4"
        >
          <input
            v-model="form.company_name"
            type="text"
            placeholder="Nom de l'entreprise"
            class="input"
            required
          />

          <textarea
            v-model="form.company_description"
            placeholder="Description de l'entreprise (optionnel)"
            class="input"
            rows="3"
          />
        </div>

        <div
          v-else
          class="space-y-4"
        >
          <input
            v-model="form.company_id"
            type="number"
            placeholder="ID de l'entreprise"
            class="input"
          />

          <p class="text-slate-400 text-xs">
            Entrez l'ID de l'entreprise fourni par votre PDG.
          </p>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full rounded-xl bg-indigo-600 py-3 text-white font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {{ loading ? "Création du compte..." : "S'inscrire" }}
        </button>
      </form>

      <p
        v-if="message"
        class="text-green-400 text-sm mt-4 text-center"
      >
        {{ message }}
      </p>

      <p
        v-if="error"
        class="text-red-400 text-sm mt-4 text-center"
      >
        {{ error }}
      </p>

      <p class="text-slate-400 text-center mt-6">
        Tu as déjà un compte ?

        <router-link
          to="/login"
          class="text-indigo-400 hover:text-indigo-300"
        >
          Se connecter
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>

import Starfield from "../components/Starfield.vue";
import { reactive, ref } from "vue";
import api from "../services/api";

const message = ref("");
const error = ref("");
const loading = ref(false);

const form = reactive({
  username: "",
  email: "",
  password: "",
  password_confirmation: "",
  role: "ceo",
  company_name: "",
  company_description: "",
  company_id: "",
});

const register = async () => {
  message.value = "";
  error.value = "";

  if (!form.username || !form.password) {
    error.value = "Veuillez remplir tous les champs obligatoires.";
    return;
  }

  if (form.password_confirmation && form.password !== form.password_confirmation) {
    error.value = "Les mots de passe ne correspondent pas.";
    return;
  }

  if (form.role === "ceo" && !form.company_name.trim()) {
    error.value = "Le nom de l'entreprise est obligatoire pour un PDG.";
    return;
  }

  try {
    loading.value = true;

    const payload = {
      username: form.username,
      email: form.email,
      password: form.password,
      password_confirmation: form.password_confirmation,
      role: form.role,
    };

    if (form.role === "ceo") {
      payload.company_name = form.company_name;
      payload.company_description = form.company_description;
    } else {
      payload.company_id = form.company_id ? Number(form.company_id) : null;
    }

    await api.post("auth/register/", payload);

    message.value = "Compte créé avec succès.";

    form.username = "";
    form.email = "";
    form.password = "";
    form.password_confirmation = "";
    form.company_name = "";
    form.company_description = "";
    form.company_id = "";

    setTimeout(() => {
      window.location.href = "/login";
    }, 1000);

  } catch (err) {
    console.error("Erreur lors de l'inscription :", err);

    error.value =
      err.response?.data?.error ||
      err.response?.data?.detail ||
      "Erreur lors de l'inscription.";

  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-page {
  position: relative;
  overflow: hidden;
}

.auth-glow {
  position: absolute;
  width: 480px;
  height: 480px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.22;
  pointer-events: none;
  animation: float-y 9s ease-in-out infinite;
}

.glow-a {
  top: -140px;
  left: -120px;
  background: #2563eb;
}

.glow-b {
  bottom: -160px;
  right: -120px;
  background: #7c3aed;
  animation-delay: -4.5s;
}

.auth-card {
  position: relative;
  z-index: 1;
  animation: scale-in 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.input {
  width: 100%;
  padding: 12px 16px;
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

select.input {
  appearance: auto;
  cursor: pointer;
}

textarea.input {
  resize: none;
  min-height: 80px;
}
</style>
