
window.onload = function () {
  const savedTheme = localStorage.getItem('theme');
  const themeToApply = savedTheme || 'theme-neon-dream'; // Default to 'theme-neon-dream'

  console.log('Saved theme from localStorage:', savedTheme);
  console.log('Applying theme:', themeToApply);

  setTheme(themeToApply);
};

function setTheme(theme) {
  // Remove all existing theme classes from the body
  const themeClasses = [
    'theme-pink-romance',
    'theme-standard',
    'theme-ocean-breeze',
    'theme-sandstorm',
    'theme-whimsical-dream',
    'theme-neon-dream',
  ];
  document.body.classList.remove(...themeClasses);

  // Apply the selected theme class
  document.body.classList.add(theme);

  // Save the selected theme to localStorage
  localStorage.setItem('theme', theme);
}
