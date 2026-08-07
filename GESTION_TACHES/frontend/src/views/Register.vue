<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-950">
    <div
      class="w-full max-w-md bg-slate-900 rounded-3xl p-8 shadow-2xl border border-slate-700"
    >
      <h1 class="text-3xl font-bold text-white text-center mb-6">
        Créer un compte
      </h1>

```
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
      v-model="form.password"
      type="password"
      placeholder="Mot de passe"
      class="input"
      required
    />

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
```

  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import api from "../services/api";

const message = ref("");
const error = ref("");
const loading = ref(false);

const form = reactive({
  username: "",
  password: "",
});

const register = async () => {
  message.value = "";
  error.value = "";

  if (!form.username || !form.password) {
    error.value = "Veuillez remplir tous les champs.";
    return;
  }

  try {
    loading.value = true;

    await api.post(
      "auth/register/",
      {
        username: form.username,
        password: form.password,
      }
    );

    message.value = "Compte créé avec succès.";

    form.username = "";
    form.password = "";

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
.input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  background: #1e293b;
  border: 1px solid #334155;
  color: white;
  outline: none;
  transition: 0.3s;
}

.input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.input::placeholder {
  color: #94a3b8;
}
</style>
