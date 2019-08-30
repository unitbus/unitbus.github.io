new Vue({
	el:"#app",
  data:{
  	listlabel:["Mens","Womens","Kids"],
    sublistlabel:["Cloth","Pants","Shoes","Goods"],
    active:""
  },
  methods:{
  	dropdown(list){
    console.log(this.active);
    	this.active = this.active===list ? "":list;
    }
  }
});

new Vue({
  el: '#app',
  mixins: [accordion], // mixinで読み込む
});
