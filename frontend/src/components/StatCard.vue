<template>

  <div class="stat-card">

    <div class="stat-info">

      <p class="stat-title">{{ title }}</p>

      <h3 class="stat-value">{{ value }}</h3>

    </div>

    <div class="stat-icon">

      <component
        :is="icon"
        :size="20"
        :stroke-width="1.8"
      />

    </div>

  </div>

</template>



<script setup>


defineProps({

title:{
type:String,
required:true
},


value:{
type:[String,Number],
required:true
},


icon:{
type:[Object,Function],
default:null
}


});

</script>



<style scoped>

.stat-card {

  background: var(--surface);

  border: 1px solid var(--border);

  border-radius: var(--radius-l);

  padding: 22px;

  display: flex;

  justify-content: space-between;

  align-items: center;

  transition: border-color .25s, transform .25s, box-shadow .25s;

}


.stat-card:hover {

  border-color: var(--accent-border);

  transform: translateY(-5px);

  box-shadow: 0 14px 34px rgba(59, 130, 246, 0.14);

}


.stat-card:hover .stat-icon {

  animation: icon-wiggle .5s ease;

  background: var(--accent);

  color: white;

}


.stat-title {

  color: var(--text);

  font-size: 13px;

  font-weight: 500;

}


.stat-value {

  color: var(--text-h);

  font-family: var(--display);

  font-size: 30px;

  font-weight: 700;

  margin-top: 8px;

}


.stat-icon {

  width: 44px;

  height: 44px;

  border-radius: var(--radius);

  display: flex;

  align-items: center;

  justify-content: center;

  background: var(--accent-soft);

  color: var(--accent);

  flex-shrink: 0;

  transition: background .25s, color .25s;

}

</style>
