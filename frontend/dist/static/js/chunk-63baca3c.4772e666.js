(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-63baca3c"],{"0894":function(e,t,r){"use strict";r.r(t);var a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return e.displayPage?r("login"):r("signup")},n=[],s=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-container",{staticClass:"fill-height"},[r("v-row",{attrs:{justify:"center",align:"center"}},[r("v-col",{attrs:{cols:"10",sm:"8",md:"6",lg:"5"}},[r("v-card",{staticClass:"pb-12 px-12 pt-6",attrs:{elevation:"24",light:""}},[r("h1",{staticClass:"text-h1 text-center mb-3"},[e._v("Sign In")]),r("v-form",{ref:"form"},[r("v-text-field",{attrs:{label:"Username",rules:[e.rules.required],outlined:!0,rounded:!0,clearable:!0,"prepend-inner-icon":"mdi-account-music"},model:{value:e.name,callback:function(t){e.name=t},expression:"name"}}),r("v-text-field",{attrs:{label:"Password",type:e.show?"text":"password",rules:[e.rules.required],outlined:!0,rounded:!0,clearable:!0,"append-icon":e.show?"mdi-eye":"mdi-eye-off","prepend-inner-icon":"mdi-key-variant"},on:{"click:append":function(t){e.show=!e.show}},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}}),e.message?r("v-alert",{attrs:{type:"error"}},[e._v(" "+e._s(e.message)+" ")]):e._e(),r("div",{staticClass:"text-center"},[r("v-btn",{attrs:{type:"submit",rounded:"",large:"",color:"primary","min-width":"150"},on:{click:e.validate}},[e._v("Login")])],1)],1),r("v-divider",{staticClass:"my-2"}),r("p",{staticClass:"text-center text-h5"},[e._v("Don't have an account?")]),r("v-btn",{attrs:{rounded:"",outlined:"",large:"",block:"",color:"secondary",to:"signup","min-width":"150"}},[e._v("Signup")])],1)],1)],1)],1)},i=[],o=(r("b0c0"),r("96cf"),r("1da1")),u={name:"Login",beforeCreate:function(){this.$store.getters["auth/getUserToken"]&&this.$router.push("/")},data:function(){return{name:"",rules:{required:function(e){return!!e||"Field is Required"}},password:"",show:!1,message:null}},methods:{validate:function(e){var t=this;return Object(o["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:if(e.preventDefault(),!t.$refs.form.validate()){r.next=4;break}return r.next=4,t.$store.dispatch("auth/loginUser",{username:t.name,password:t.password}).then((function(){return t.$router.push("/")})).catch((function(e){return t.message=e.message}));case 4:case"end":return r.stop()}}),r)})))()}}},l=u,c=(r("b4b3"),r("2877")),d=r("6544"),p=r.n(d),h=r("0798"),m=r("8336"),f=r("b0af"),v=r("62ad"),w=r("a523"),g=r("ce7e"),b=(r("4de4"),r("7db0"),r("4160"),r("caad"),r("07ac"),r("2532"),r("159b"),r("5530")),x=r("58df"),_=r("7e2b"),y=r("3206"),V=Object(x["a"])(_["a"],Object(y["b"])("form")).extend({name:"v-form",provide:function(){return{form:this}},inheritAttrs:!1,props:{disabled:Boolean,lazyValidation:Boolean,readonly:Boolean,value:Boolean},data:function(){return{inputs:[],watchers:[],errorBag:{}}},watch:{errorBag:{handler:function(e){var t=Object.values(e).includes(!0);this.$emit("input",!t)},deep:!0,immediate:!0}},methods:{watchInput:function(e){var t=this,r=function(e){return e.$watch("hasError",(function(r){t.$set(t.errorBag,e._uid,r)}),{immediate:!0})},a={_uid:e._uid,valid:function(){},shouldValidate:function(){}};return this.lazyValidation?a.shouldValidate=e.$watch("shouldValidate",(function(n){n&&(t.errorBag.hasOwnProperty(e._uid)||(a.valid=r(e)))})):a.valid=r(e),a},validate:function(){return 0===this.inputs.filter((function(e){return!e.validate(!0)})).length},reset:function(){this.inputs.forEach((function(e){return e.reset()})),this.resetErrorBag()},resetErrorBag:function(){var e=this;this.lazyValidation&&setTimeout((function(){e.errorBag={}}),0)},resetValidation:function(){this.inputs.forEach((function(e){return e.resetValidation()})),this.resetErrorBag()},register:function(e){this.inputs.push(e),this.watchers.push(this.watchInput(e))},unregister:function(e){var t=this.inputs.find((function(t){return t._uid===e._uid}));if(t){var r=this.watchers.find((function(e){return e._uid===t._uid}));r&&(r.valid(),r.shouldValidate()),this.watchers=this.watchers.filter((function(e){return e._uid!==t._uid})),this.inputs=this.inputs.filter((function(e){return e._uid!==t._uid})),this.$delete(this.errorBag,t._uid)}}},render:function(e){var t=this;return e("form",{staticClass:"v-form",attrs:Object(b["a"])({novalidate:!0},this.attrs$),on:{submit:function(e){return t.$emit("submit",e)}}},this.$slots.default)}}),$=r("0fd9"),C=r("8654"),k=Object(c["a"])(l,s,i,!1,null,null,null),B=k.exports;p()(k,{VAlert:h["a"],VBtn:m["a"],VCard:f["a"],VCol:v["a"],VContainer:w["a"],VDivider:g["a"],VForm:V,VRow:$["a"],VTextField:C["a"]});var R=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-container",{staticClass:"fill-height"},[r("v-row",{attrs:{justify:"center",align:"center"}},[r("v-col",{attrs:{cols:"10",sm:"8",md:"6",lg:"5"}},[r("v-card",{staticClass:"pb-12 px-12 pt-6",attrs:{elevation:"12",light:""}},[r("h1",{staticClass:"text-h1 text-center mb-3"},[e._v("Sign Up")]),r("v-form",{ref:"form"},[r("v-text-field",{attrs:{rules:[e.rules.required,e.rules.nameRule],label:"Username",outlined:!0,rounded:!0,clearable:!0,"prepend-inner-icon":"mdi-account-music"},model:{value:e.name,callback:function(t){e.name=t},expression:"name"}}),r("v-text-field",{attrs:{rules:[e.rules.required,e.rules.emailRule],label:"Email",outlined:!0,type:"email",rounded:!0,clearable:!0,"prepend-inner-icon":"mdi-email"},model:{value:e.email,callback:function(t){e.email=t},expression:"email"}}),r("v-text-field",{attrs:{rules:[e.rules.required,e.rules.passRule],label:"Password",type:e.show?"text":"password",outlined:!0,rounded:!0,clearable:!0,"append-icon":e.show?"mdi-eye":"mdi-eye-off","prepend-inner-icon":"mdi-key-variant"},on:{"click:append":function(t){e.show=!e.show}},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}}),r("v-text-field",{attrs:{rules:[e.rules.required,e.passComp],label:"Confirm Password",type:e.show2?"text":"password",outlined:!0,rounded:!0,clearable:!0,"append-icon":e.show2?"mdi-eye":"mdi-eye-off","prepend-inner-icon":"mdi-key-variant"},on:{"click:append":function(t){e.show2=!e.show2}},model:{value:e.password2,callback:function(t){e.password2=t},expression:"password2"}}),e.message?r("v-alert",{attrs:{type:"error"}},[e._v(" "+e._s(e.message)+" ")]):e._e(),r("div",{staticClass:"text-center"},[r("v-btn",{attrs:{type:"submit",rounded:"",large:"",color:"primary","min-width":"150"},on:{click:e.validate}},[e._v("Signup")])],1)],1),r("v-divider",{staticClass:"my-2"}),r("p",{staticClass:"text-center"},[e._v("Have an account? "),r("router-link",{attrs:{to:"login",tag:"a"}},[r("a",[e._v("Log in")])])],1)],1)],1)],1)],1)},E=[],j={name:"Signup",beforeCreate:function(){this.$store.getters["auth/getUserToken"]&&this.$router.push("/")},data:function(){return{name:"",rules:{required:function(e){return!!e||"Field is Required"},nameRule:function(e){return/^[-\w.$@*!]{5,30}$/.test(e)||"Incorrect Input"},emailRule:function(e){return/.+@.+\..+/.test(e)||"E-mail must be valid"},passRule:function(e){return/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z_@./#&+-]{8,}$/.test(e)||"Password must be alphanumeric having atleast one Uppercase character"}},password:"",password2:"",email:"",show:!1,show2:!1,message:null}},computed:{passComp:function(){var e=this;return function(){return e.password===e.password2||"Password doesnt match"}}},methods:{validate:function(e){var t=this;e.preventDefault(),this.$refs.form.validate()&&this.$store.dispatch("auth/registerUser",{username:this.name,password:this.password,password2:this.password2,email:this.email}).then((function(){t.$router.push("/login")})).catch((function(e){return t.message=e.message}))}}},q=j,O=Object(c["a"])(q,R,E,!1,null,null,null),P=O.exports;p()(O,{VAlert:h["a"],VBtn:m["a"],VCard:f["a"],VCol:v["a"],VContainer:w["a"],VDivider:g["a"],VForm:V,VRow:$["a"],VTextField:C["a"]});var U={components:{login:B,signup:P},computed:{displayPage:function(){return"/login"===this.$route.path}}},F=U,z=Object(c["a"])(F,a,n,!1,null,null,null);t["default"]=z.exports},"54c1":function(e,t,r){},b4b3:function(e,t,r){"use strict";var a=r("54c1"),n=r.n(a);n.a}}]);
//# sourceMappingURL=chunk-63baca3c.4772e666.js.map