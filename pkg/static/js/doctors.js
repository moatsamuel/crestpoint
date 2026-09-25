/**
 * CrestPoint Clinic — Doctors Directory Search & Filter Module
 */

document.addEventListener('DOMContentLoaded', () => {
  const doctorGrid = document.getElementById('doctors-directory-grid');
  if (!doctorGrid) return;

  const searchInput = document.getElementById('search-doctor-input');
  const specialtyFilter = document.getElementById('specialty-filter');
  const availabilityFilter = document.getElementById('availability-filter');

  const doctors = JSON.parse(localStorage.getItem('crest_doctors') || '[]');

  // Check URL parameters for specialty filter
  const urlParams = new URLSearchParams(window.location.search);
  const paramSpecialty = urlParams.get('specialty');
  if (paramSpecialty && specialtyFilter) {
    specialtyFilter.value = paramSpecialty;
  }

  function renderDoctors() {
    const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const selectedSpecialty = specialtyFilter ? specialtyFilter.value.toLowerCase() : 'all';
    const selectedAvailability = availabilityFilter ? availabilityFilter.value.toLowerCase() : 'all';

    const filtered = doctors.filter(d => {
      const matchesSearch = d.name.toLowerCase().includes(searchTerm) || d.specialty.toLowerCase().includes(searchTerm);
      const matchesSpecialty = selectedSpecialty === 'all' || d.specialtyId === selectedSpecialty || d.specialty.toLowerCase() === selectedSpecialty;
      const matchesAvailability = selectedAvailability === 'all' || 
        (selectedAvailability === 'today' && d.availability.toLowerCase().includes('today')) ||
        (selectedAvailability === 'week' && (d.availability.toLowerCase().includes('week') || d.availability.toLowerCase().includes('today')));

      return matchesSearch && matchesSpecialty && matchesAvailability;
    });

    if (!filtered.length) {
      doctorGrid.innerHTML = `
        <div class="col-span-full text-center py-16 bg-gray-50 dark:bg-slate-800/40 rounded-2xl border border-dashed border-gray-300 dark:border-slate-700">
          <i data-lucide="user-x" class="w-12 h-12 text-gray-400 mx-auto mb-3"></i>
          <h4 class="text-base font-bold text-gray-900 dark:text-white">No Healthcare Professionals Found</h4>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Try resetting your filters or search terms.</p>
        </div>
      `;
      if (window.lucide) window.lucide.createIcons();
      return;
    }

    doctorGrid.innerHTML = filtered.map(d => `
      <div class="doctor-card bg-white dark:bg-slate-800 rounded-2xl p-6 border border-gray-100 dark:border-slate-700/60 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between">
        <div>
          <div class="relative mb-4">
            <img src="${d.image}" alt="${d.name}" class="w-full h-48 rounded-xl object-cover">
            <span class="absolute top-3 right-3 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md px-2.5 py-1 rounded-full text-xs font-bold text-amber-500 shadow-sm flex items-center gap-1">
              ★ ${d.rating} <span class="text-gray-400 font-normal">(${d.reviewsCount})</span>
            </span>
          </div>

          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">${d.specialty}</span>
            <span class="text-xs font-medium ${d.availability.includes('Today') ? 'text-green-600 bg-green-50 dark:bg-green-900/30' : 'text-blue-600 bg-blue-50 dark:bg-blue-900/30'} px-2 py-0.5 rounded-full">
              ${d.availability}
            </span>
          </div>

          <h3 class="text-lg font-bold text-gray-900 dark:text-white">${d.name}</h3>

          <div class="mt-3 space-y-1 text-xs text-gray-600 dark:text-gray-300">
            <div class="flex items-center gap-2">
              <i data-lucide="award" class="w-4 h-4 text-gray-400"></i>
              <span>${d.experience} Years Experience</span>
            </div>
            <div class="flex items-center gap-2">
              <i data-lucide="languages" class="w-4 h-4 text-gray-400"></i>
              <span>${d.languages.join(', ')}</span>
            </div>
            <div class="flex items-center gap-2">
              <i data-lucide="credit-card" class="w-4 h-4 text-gray-400"></i>
              <span>Consultation Fee: <strong>$${d.fee}</strong></span>
            </div>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t border-gray-100 dark:border-slate-700/60 flex items-center gap-2">
          <a href="doctor-profile.html?id=${d.id}" class="flex-1 text-center py-2 px-3 border border-indigo-600 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded-xl text-xs font-semibold transition-all">
            View Profile
          </a>
          <a href="appointments.html?doctor=${d.id}&specialty=${d.specialtyId}" class="flex-1 text-center py-2 px-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm transition-all">
            Book Appointment
          </a>
        </div>
      </div>
    `).join('');

    if (window.lucide) window.lucide.createIcons();
  }

  if (searchInput) searchInput.addEventListener('input', renderDoctors);
  if (specialtyFilter) specialtyFilter.addEventListener('change', renderDoctors);
  if (availabilityFilter) availabilityFilter.addEventListener('change', renderDoctors);

  renderDoctors();
});
