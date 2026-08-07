<template>

  <div
    class="bg-slate-900 rounded-3xl p-6 border border-slate-700 shadow-xl hover:shadow-2xl transition"
  >

    <div class="flex justify-between items-center">


      <div>

        <p class="text-slate-400 text-sm">
          {{ title }}
        </p>


        <h3 class="text-3xl font-bold text-white mt-3">
          {{ value }}
        </h3>


      </div>



      <div
        class="text-3xl"
      >
        {{ icon }}
      </div>


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
type:String,
default:"📊"
}


});


</script>