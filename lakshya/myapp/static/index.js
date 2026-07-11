let jobs = [
//   { title: "Frontend Developer", company: "Google", location: "Remote", salary: "$120k" },
//   { title: "Product Designer", company: "Figma", location: "San Francisco, CA", salary: "$135k" },
//   { title: "Backend Engineer", company: "Stripe", location: "New York, NY", salary: "$145k" },
//   { title: "Data Analyst", company: "Netflix", location: "Remote", salary: "$110k" },
//   { title: "DevOps Engineer", company: "Amazon", location: "Seattle, WA", salary: "$150k" },
//   { title: "Marketing Manager", company: "Airbnb", location: "Remote", salary: "$98k" },
];

const jobsGrid = document.getElementById("jobsGrid");
const emptyState = document.getElementById("emptyState");
const addJobBtn = document.getElementById("addJobBtn");

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function createJobCard(job, index) {
  const card = document.createElement("div");
  card.className =
    "job-card bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-md p-5 flex flex-col gap-3";

  card.innerHTML = `
    <div class="flex items-start justify-between gap-2">
      <div>
        <h3 class="font-semibold text-slate-900">${escapeHtml(job.title)}</h3>
        <p class="text-sm text-slate-500">${escapeHtml(job.company)}</p>
      </div>
      <span class="text-xs font-medium bg-emerald-50 text-emerald-600 px-2 py-1 rounded-full whitespace-nowrap flex items-center gap-1">
        <span class="material-icons-outlined text-sm">check_circle</span>
        Hiring
      </span>
    </div>

    <div class="flex items-center gap-4 text-sm text-slate-500">
      <span class="flex items-center gap-1">
        <span class="material-icons-outlined text-base">location_on</span>
        ${escapeHtml(job.location)}
      </span>
      <span class="font-medium text-slate-700 flex items-center gap-1">
        <span class="material-icons-outlined text-base">attach_money</span>
        ${escapeHtml(job.salary)}
      </span>
    </div>

    <div class="flex justify-end pt-2 border-t border-slate-100">
      <button
        class="delete-btn text-sm text-slate-400 hover:text-red-600 transition-colors flex items-center gap-1"
      >
        <span class="material-icons-outlined text-sm leading-none">delete</span>
        Delete
      </button>
    </div>
  `;

  card.querySelector(".delete-btn").addEventListener("click", () => {
    jobs.splice(index, 1);
    renderJobs();
  });

  return card;
}

function renderJobs() {
  jobsGrid.innerHTML = "";
  jobs.forEach((job, index) => jobsGrid.appendChild(createJobCard(job, index)));

  const hasJobs = jobs.length > 0;
  jobsGrid.classList.toggle("hidden", !hasJobs);
  emptyState.classList.toggle("hidden", hasJobs);
}

function addJob() {
  const title = prompt("Job title:");
  if (!title) return;

  const company = prompt("Company name:");
  if (!company) return;

  const location = prompt("Location:");
  if (!location) return;

  const salary = prompt("Salary:");
  if (!salary) return;

  jobs.push({ title, company, location, salary });
  renderJobs();
}

addJobBtn.addEventListener("click", addJob);

renderJobs();