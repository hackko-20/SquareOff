const intro = document.querySelector('.intro');
const video = intro.querySelector('video');
const section = document.querySelector('section');
const end = section.querySelector('h1');
const controller = new ScrollMagic.Controller();

let scene = new ScrollMagic.Scene({
    duration:9000,
    triggerElement:intro,
    triggerHook:0
})
.addIndicators()
.setPin(intro)
.addTo(controller);
const textAnim = TweenMax.fromTo(".text",2,{opacity:1},{opacity:0});
let scene2 = new ScrollMagic.Scene({
    duration:1000,
    triggerElement:intro,
    triggerHook:0
})
.setTween(textAnim)
.addTo(controller);
const textAnim2 = new TimelineMax().fromTo(".text2",0.1,{opacity:0},{opacity:1}).to(".text2",0.1,{opacity:0}).fromTo(".text3",0.1,{opacity:0},{opacity:1}).to(".text3",0.1,{opacity:0}).fromTo(".text4",0.1,{opacity:0},{opacity:1}).to(".text4",0.1,{opacity:0});
let scene3 = new ScrollMagic.Scene({
    duration:9000,
    triggerElement:intro,
    triggerHook:0
})
.setTween(textAnim2)
.addTo(controller);
let accelamount=0.1;
let scrollpos=0;
let delay=0;

scene.on("update",e=>{
    scrollpos = e.scrollPos/1000;
});
setInterval(()=>{
    delay+=(scrollpos-delay)*accelamount;
    video.currentTime=scrollpos;
},33.3);
