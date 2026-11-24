<template>

  <aside
    class="sidebar"
    :class="{open: props.open}"
    @click="emit('close')"
  >
    <!-- LOGO -->

    <div class="brand">

      <h1>NOVA TASKS</h1>

      <p>Pilotage d'entreprise</p>

      <span class="brand-signature">by Clever</span>

    </div>



    <!-- NAVIGATION -->

    <nav class="menu" @click.stop>

      <RouterLink
        v-for="item in menuItems"
        :key="item.to"
        :to="item.to"
        class="menu-item"
      >
        <span class="item-index">{{ item.index }}</span>
        <component :is="item.icon" :size="18" :stroke-width="1.8" class="icon" />
        <span class="item-label">{{ item.label }}</span>
      </RouterLink>

    </nav>



    <!-- PROFIL -->

    <div class="profile">


      <div class="avatar">

        {{ initial }}

      </div>



      <div class="user-info">

        <p class="username">
          {{ username }}
        </p>


        <p class="status">

          <span></span>
          {{ roleLabel }}

        </p>


      </div>


    </div>


  </aside>


</template>



<script setup>
import { computed } from "vue";
import {
  LayoutDashboard,
  ClipboardList,
  CalendarDays,
  BarChart3,
  Trash2,
  Building2,
  Bell,
} from "lucide-vue-next";

const props = defineProps({

  open: {
    type: Boolean,
    default: false
  }

});

const username =
  localStorage.getItem("username")
  || "Utilisateur";

const isCEO = localStorage.getItem("is_ceo") === "1";

const roleLabel = computed(() => {

  return isCEO ? "PDG" : "Employé";

});

const initial = computed(() => {

  return username
    .charAt(0)
    .toUpperCase();

});

const baseItems = [
  { to: "/dashboard",     label: "Tableau de bord", icon: LayoutDashboard },
  { to: "/tasks",         label: "Gestion tâches",  icon: ClipboardList },
  { to: "/calendar",      label: "Calendrier",      icon: CalendarDays },
  { to: "/statistics",    label: "Statistiques",    icon: BarChart3 },
  { to: "/archives",      label: "Corbeille",       icon: Trash2 },
];

const menuItems = computed(() => {

  const items = [...baseItems];

  if (isCEO) {

    items.push({
      to: "/company",
      label: "Mon entreprise",
      icon: Building2,
    });

  }

  items.push({
    to: "/notifications",
    label: "Notifications",
    icon: Bell,
  });

  return items.map((item, i) => ({
    ...item,
    index: String(i + 1).padStart(2, "0"),
  }));

});

const emit = defineEmits([
  "close"
]);
</script>



<style scoped>


.sidebar {

  width: 280px;

  height: 100vh;

  position: sticky;

  top: 0;

  flex-shrink: 0;

  background: var(--surface);

  border-right: 1px solid var(--border);

  display: flex;

  flex-direction: column;

  padding: 28px 20px;

}


/* BRAND */


.brand {
  padding: 0 8px;
  flex-shrink: 0;
}


.brand h1 {

  color: var(--text-h);

  font-family: var(--display);

  font-size: 24px;

  font-weight: 700;

  letter-spacing: 2px;

}


.brand p {

  margin-top: 6px;

  color: var(--text);

  font-size: 13px;

}


.brand-signature {

  display: block;

  margin-top: 6px;

  color: var(--accent);

  font-size: 13px;

  font-weight: 700;

  letter-spacing: 1px;

}


/* MENU */


.menu {

  margin-top: 40px;

  display: flex;

  flex-direction: column;

  gap: 6px;

  flex: 1;

  min-height: 0;

  overflow-y: auto;

  padding-right: 4px;

}


.menu-item {

  display: flex;

  align-items: center;

  gap: 14px;

  padding: 13px 14px;

  border-radius: var(--radius);

  color: var(--text);

  text-decoration: none;

  font-weight: 500;

  font-size: 14px;

  border: 1px solid transparent;

  transition: background .2s, color .2s, border-color .2s;

}


.item-index {

  font-family: var(--display);

  font-size: 11px;

  font-weight: 600;

  color: var(--text);

  opacity: .5;

  width: 20px;

  flex-shrink: 0;

}


.menu-item .icon {

  flex-shrink: 0;

}


.menu-item:hover {

  background: var(--surface-2);

  color: var(--text-h);

  border-color: var(--border);

}


.menu-item:hover .item-index {

  color: var(--accent);

  opacity: 1;

}


/* PAGE ACTIVE */


.router-link-active {

  background: var(--accent-soft);

  border-color: var(--accent-border);

  color: var(--text-h);

}


.router-link-active .item-index {

  color: var(--accent);

  opacity: 1;

}


.router-link-active .icon {

  color: var(--accent);

}


/* PROFIL */


.profile {

  display: flex;

  align-items: center;

  gap: 14px;

  padding: 20px 8px 0;

  border-top: 1px solid var(--border);

  flex-shrink: 0;

}


.avatar {

  width: 44px;

  height: 44px;

  border-radius: 50%;

  display: flex;

  align-items: center;

  justify-content: center;

  background: var(--accent-strong);

  color: white;

  font-family: var(--display);

  font-weight: 700;

  font-size: 17px;

}


.username {

  color: var(--text-h);

  font-weight: 600;

}


.status {

  display: flex;

  align-items: center;

  gap: 6px;

  color: var(--success);

  font-size: 12px;

}


.status span {

  width: 7px;

  height: 7px;

  border-radius: 50%;

  background: var(--success);

}


@media (min-width:769px) and (max-width:900px){

  .sidebar{

    position: fixed;

    left: -300px;

    top: 0;

    z-index: 1000;

    transition: .3s;

  }

  .sidebar.open{

    left: 0;

  }

}


@media (max-width:768px){


  .sidebar{

    position: fixed;

    left: -300px;

    top: 0;

    z-index: 1000;

    transition: .3s;

  }


  .sidebar.open{

    left: 0;

  }


}


</style>
