<template>

  <div
    class="bg-slate-900 rounded-3xl p-6 border border-slate-700 shadow-xl"
  >

    <h2 class="text-xl font-bold text-white mb-6">
      📊 Progression des tâches
    </h2>


    <div class="space-y-5">


      <div>

        <div class="flex justify-between text-sm mb-2">

          <span class="text-slate-300">
            À faire
          </span>

          <span class="text-white">
            {{ todo }}
          </span>

        </div>


        <div class="h-3 bg-slate-700 rounded-full">

          <div
            class="h-3 bg-indigo-500 rounded-full transition-all"
            :style="{width: percentage(todo) + '%'}"
          ></div>

        </div>


      </div>




      <div>

        <div class="flex justify-between text-sm mb-2">

          <span class="text-slate-300">
            En cours
          </span>


          <span class="text-white">
            {{ progress }}
          </span>


        </div>


        <div class="h-3 bg-slate-700 rounded-full">

          <div
            class="h-3 bg-orange-500 rounded-full transition-all"
            :style="{width: percentage(progress) + '%'}"
          ></div>


        </div>


      </div>





      <div>


        <div class="flex justify-between text-sm mb-2">

          <span class="text-slate-300">
            Terminées
          </span>


          <span class="text-white">
            {{ done }}
          </span>


        </div>


        <div class="h-3 bg-slate-700 rounded-full">


          <div
            class="h-3 bg-green-500 rounded-full transition-all"
            :style="{width: percentage(done) + '%'}"
          ></div>


        </div>


      </div>



    </div>


  </div>


</template>



<script setup>


const props = defineProps({

todo:{
type:Number,
default:0
},


progress:{
type:Number,
default:0
},


done:{
type:Number,
default:0
}

});



const total = () => {

return props.todo + props.progress + props.done || 1;

};



const percentage = (value)=>{

return Math.round(
(value / total()) * 100
);

};



</script>