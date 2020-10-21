(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-63baca3c"],{"0894":function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return e.displayPage?a("login"):a("signup")},s=[],n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-container",{staticClass:"fill-height"},[a("v-row",{attrs:{justify:"center",align:"center"}},[a("v-col",{attrs:{cols:"10",sm:"8",md:"6",lg:"5"}},[a("v-card",{staticClass:"pb-12 px-12 pt-6",attrs:{elevation:"24",light:""}},[a("v-img",{staticClass:"mb-8 mx-auto",attrs:{src:e.image,"aspect-ratio":1,width:"60%"}}),a("v-form",{ref:"form"},[a("v-text-field",{attrs:{label:"Username",rules:[e.rules.required],outlined:!0,rounded:!0,clearable:!0,"prepend-inner-icon":"mdi-account-music"},model:{value:e.name,callback:function(t){e.name=t},expression:"name"}}),a("v-text-field",{attrs:{label:"Password",type:e.show?"text":"password",rules:[e.rules.required],outlined:!0,rounded:!0,clearable:!0,"append-icon":e.show?"mdi-eye":"mdi-eye-off","prepend-inner-icon":"mdi-key-variant"},on:{"click:append":function(t){e.show=!e.show}},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}}),e.message?a("v-alert",{attrs:{type:"error"}},[e._v(" "+e._s(e.message)+" ")]):e._e(),a("div",{staticClass:"text-center"},[a("v-btn",{attrs:{type:"submit",rounded:"",large:"",color:"primary","min-width":"150"},on:{click:e.validate}},[e._v("Login")])],1)],1),a("v-divider",{staticClass:"my-2"}),a("p",{staticClass:"text-center text-h5"},[e._v("Don't have an account?")]),a("v-btn",{attrs:{rounded:"",outlined:"",large:"",block:"",color:"secondary",to:"signup","min-width":"150"}},[e._v("Signup")])],1)],1)],1)],1)},i=[],o=(a("b0c0"),a("96cf"),a("1da1")),l={name:"Login",beforeCreate:function(){this.$store.getters["auth/getUserToken"]&&this.$router.push("/")},data:function(){return{name:"",rules:{required:function(e){return!!e||"Field is Required"}},password:"",show:!1,message:null,image:a("d2f4")}},methods:{validate:function(e){var t=this;return Object(o["a"])(regeneratorRuntime.mark((function a(){return regeneratorRuntime.wrap((function(a){while(1)switch(a.prev=a.next){case 0:if(e.preventDefault(),!t.$refs.form.validate()){a.next=4;break}return a.next=4,t.$store.dispatch("auth/loginUser",{username:t.name,password:t.password}).then((function(){return t.$router.push("/")})).catch((function(e){return t.message=e.message}));case 4:case"end":return a.stop()}}),a)})))()}}},u=l,c=(a("b4b3"),a("2877")),d=a("6544"),p=a.n(d),m=a("0798"),f=a("8336"),v=a("b0af"),h=a("62ad"),w=a("a523"),g=a("ce7e"),b=a("4bd4"),x=a("adda"),y=a("0fd9"),k=a("8654"),C=Object(c["a"])(u,n,i,!1,null,null,null),V=C.exports;p()(C,{VAlert:m["a"],VBtn:f["a"],VCard:v["a"],VCol:h["a"],VContainer:w["a"],VDivider:g["a"],VForm:b["a"],VImg:x["a"],VRow:y["a"],VTextField:k["a"]});var _=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-container",{staticClass:"fill-height"},[a("v-row",{attrs:{justify:"center",align:"center"}},[a("v-col",{attrs:{cols:"10",sm:"8",md:"6",lg:"5"}},[a("v-card",{staticClass:"pb-12 px-12 pt-6",attrs:{elevation:"12",light:""}},[a("v-img",{staticClass:"mb-8 mx-auto",attrs:{src:e.image,"aspect-ratio":1,width:"60%"}}),a("v-form",{ref:"form"},[a("v-text-field",{attrs:{rules:[e.rules.required,e.rules.nameRule],label:"Username",outlined:!0,rounded:!0,clearable:!0,"prepend-inner-icon":"mdi-account-music"},model:{value:e.name,callback:function(t){e.name=t},expression:"name"}}),a("v-text-field",{attrs:{rules:[e.rules.required,e.rules.emailRule],label:"Email",outlined:!0,type:"email",rounded:!0,clearable:!0,"prepend-inner-icon":"mdi-email"},model:{value:e.email,callback:function(t){e.email=t},expression:"email"}}),a("v-text-field",{attrs:{rules:[e.rules.required,e.rules.passRule],label:"Password",type:e.show?"text":"password",outlined:!0,rounded:!0,clearable:!0,"append-icon":e.show?"mdi-eye":"mdi-eye-off","prepend-inner-icon":"mdi-key-variant"},on:{"click:append":function(t){e.show=!e.show}},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}}),a("v-text-field",{attrs:{rules:[e.rules.required,e.passComp],label:"Confirm Password",type:e.show2?"text":"password",outlined:!0,rounded:!0,clearable:!0,"append-icon":e.show2?"mdi-eye":"mdi-eye-off","prepend-inner-icon":"mdi-key-variant"},on:{"click:append":function(t){e.show2=!e.show2}},model:{value:e.password2,callback:function(t){e.password2=t},expression:"password2"}}),e.message?a("v-alert",{attrs:{type:"error"}},[e._v(" "+e._s(e.message)+" ")]):e._e(),a("div",{staticClass:"text-center"},[a("v-btn",{attrs:{type:"submit",rounded:"",large:"",color:"primary","min-width":"150"},on:{click:e.validate}},[e._v("Signup")])],1)],1),a("v-divider",{staticClass:"my-2"}),a("p",{staticClass:"text-center"},[e._v("Have an account? "),a("router-link",{attrs:{to:"login",tag:"a"}},[a("a",[e._v("Log in")])])],1)],1)],1)],1)],1)},$=[],R={name:"Signup",beforeCreate:function(){this.$store.getters["auth/getUserToken"]&&this.$router.push("/")},data:function(){return{name:"",rules:{required:function(e){return!!e||"Field is Required"},nameRule:function(e){return/^[-\w.$@*!]{5,30}$/.test(e)||"Incorrect Input"},emailRule:function(e){return/.+@.+\..+/.test(e)||"E-mail must be valid"},passRule:function(e){return/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z_@./#&+-]{8,}$/.test(e)||"Password must be alphanumeric having atleast one Uppercase character"}},password:"",password2:"",email:"",show:!1,show2:!1,message:null,image:a("d2f4")}},computed:{passComp:function(){var e=this;return function(){return e.password===e.password2||"Password doesnt match"}}},methods:{validate:function(e){var t=this;e.preventDefault(),this.$refs.form.validate()&&this.$store.dispatch("auth/registerUser",{username:this.name,password:this.password,password2:this.password2,email:this.email}).then((function(){t.$router.push("/login")})).catch((function(e){return t.message=e.message}))}}},q=R,P=Object(c["a"])(q,_,$,!1,null,null,null),U=P.exports;p()(P,{VAlert:m["a"],VBtn:f["a"],VCard:v["a"],VCol:h["a"],VContainer:w["a"],VDivider:g["a"],VForm:b["a"],VImg:x["a"],VRow:y["a"],VTextField:k["a"]});var j={components:{login:V,signup:U},computed:{displayPage:function(){return"/login"===this.$route.path}}},F=j,D=Object(c["a"])(F,r,s,!1,null,null,null);t["default"]=D.exports},"54c1":function(e,t,a){},b4b3:function(e,t,a){"use strict";var r=a("54c1"),s=a.n(r);s.a}}]);
//# sourceMappingURL=chunk-63baca3c.afab5f64.js.map