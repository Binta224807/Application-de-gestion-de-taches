<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-950">
    <div
      class="w-full max-w-md bg-slate-900 p-8 rounded-3xl border border-slate-700 shadow-xl"
    >
      <h1 class="text-3xl font-bold text-white text-center mb-8">
        Connexion
      </h1>

```
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
```

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

    const response = await api.post(
      "auth/login/",
      {
        username: form.username,
        password: form.password,
      }
    );

    const accessToken = response.data.access;
    const refreshToken = response.data.refresh;

    if (!accessToken || !refreshToken) {
      throw new Error("Tokens JWT manquants dans la réponse.");
    }

    localStorage.setItem(
      "access",
      accessToken
    );

    localStorage.setItem(
      "refresh",
      refreshToken
    );

    localStorage.setItem(
      "username",
      form.username
    );

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
.input {
  width: 100%;
  padding: 12px;
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



