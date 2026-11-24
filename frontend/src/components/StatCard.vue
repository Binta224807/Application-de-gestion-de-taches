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

  transition: border-color .2s, transform .2s;

}


.stat-card:hover {

  border-color: var(--border-strong);

  transform: translateY(-2px);

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

}

</style>
