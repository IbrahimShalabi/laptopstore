document.addEventListener("DOMContentLoaded", function() {
  const sections = document.querySelectorAll('.section');

  // إظهار القسم الأول فقط وإخفاء البقية
  sections.forEach((section, index) => {
      if (index === 0) {
          section.style.display = 'block'; // إظهار أول قسم فقط
      } else {
          section.style.display = 'none'; // إخفاء البقية
      }
  });

  // إضافة وظيفة التنقل بين الأقسام عند النقر على الروابط الداخلية فقط
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
      link.addEventListener('click', function(e) {
          const targetSectionId = link.getAttribute('href');

          // التأكد من أن الرابط داخلي (يبدأ بـ #) وإلا فإنه رابط خارجي
          if (targetSectionId.startsWith("#")) {
              e.preventDefault(); // منع الانتقال الفعلي فقط للروابط الداخلية
              const sectionId = targetSectionId.substring(1); // إزالة #
              
              // إخفاء كل الأقسام
              sections.forEach(section => {
                  section.style.display = 'none';
              });

              // إظهار القسم المستهدف
              const targetSection = document.getElementById(sectionId);
              if (targetSection) {
                  targetSection.style.display = 'block';
              }
          }
      });
  });
});
