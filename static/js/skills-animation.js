// Animate skill bars when section is visible
document.addEventListener('DOMContentLoaded', function(){
  function isInViewport(el){
    const rect = el.getBoundingClientRect();
    return rect.top < (window.innerHeight || document.documentElement.clientHeight) && rect.bottom >= 0;
  }
  const section = document.getElementById('skills-section');
  if(!section) return;
  let animated = false;
  function animate(){
    if(animated) return;
    if(isInViewport(section)){
      document.querySelectorAll('.skill-bar > span').forEach((el, i)=>{
        const w = el.getAttribute('data-width') || '70%';
        setTimeout(()=>{ el.style.transition = 'width 1.2s ease'; el.style.width = w; }, i*100);
      });
      animated = true;
    }
  }
  window.addEventListener('scroll', animate);
  animate();
});
