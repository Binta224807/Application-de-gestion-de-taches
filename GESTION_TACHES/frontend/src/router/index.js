import { createRouter, createWebHistory } from "vue-router";

import Login from "../views/Login.vue";
import Register from "../views/Register.vue";

import Calendar from "../pages/Calendar.vue";
import Statistics from "../pages/Statistics.vue";
import Archives from "../pages/Archives.vue";

import TableauDeBord from "../pages/TableauDeBord.vue";
import Kanban from "../pages/kanban.vue";


const routes = [

  {
    path: "/",
    redirect: "/login"
  },


  {
    path: "/login",
    name: "Login",
    component: Login
  },


  {
    path: "/register",
    name: "Register",
    component: Register
  },


  {
    path: "/dashboard",
    name: "Dashboard",
    component: TableauDeBord,
    meta: {
      requiresAuth: true
    }
  },


  {
    path: "/kanban",
    name: "Kanban",
    component: Kanban,
    meta: {
      requiresAuth: true
    }
  },


  {
    path: "/calendar",
    name: "Calendar",
    component: Calendar,
    meta: {
      requiresAuth: true
    }
  },


  {
    path: "/statistics",
    name: "Statistics",
    component: Statistics,
    meta: {
      requiresAuth: true
    }
  },


  {
    path: "/archives",
    name: "Archives",
    component: Archives,
    meta: {
      requiresAuth: true
    }
  }

];


const router = createRouter({
  history: createWebHistory(),
  routes
});


// Protection des pages
router.beforeEach((to, from, next) => {

  const token = localStorage.getItem("access","access_token");


  if (to.meta.requiresAuth && !token) {
    next("/login");
  }

  else if (to.path === "/login" && token) {
    next("/dashboard");
  }

  else {
    next();
  }

});


export default router;