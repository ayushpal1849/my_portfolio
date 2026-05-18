const routes = {
    "/": "home",
    "/about": "about",
    "/education": "education",
    "/skills": "skills",
    "/experience": "experience",
    "/projects": "projects",
    "/certifications": "certifications",
    "/contact": "contact",
};

const titles = {
    home: "Home",
    about: "About",
    education: "Education",
    skills: "Skills",
    experience: "Experience",
    projects: "Projects",
    certifications: "Certifications",
    contact: "Contact",
};

const appState = {
    data: null,
    activeCertIndex: 0,
    roleIntervalId: null,
    navOpen: false,
};

const appRoot = document.getElementById("app");
const progressBar = document.getElementById("shell-progress");
const navPanel = document.querySelector("[data-nav-panel]");
const navToggle = document.querySelector("[data-nav-toggle]");

function initParticles() {
    tsParticles.load("tsparticles", {
        fullScreen: { enable: false },
        background: { color: { value: "transparent" } },
        particles: {
            number: { value: 72, density: { enable: true, area: 920 } },
            color: { value: ["#78e7ff", "#f4cb74"] },
            shape: { type: "circle" },
            opacity: { value: 0.22 },
            size: { value: { min: 1, max: 4 } },
            links: {
                enable: true,
                distance: 150,
                color: "#78e7ff",
                opacity: 0.14,
                width: 1,
            },
            move: {
                enable: true,
                speed: 1,
                outModes: { default: "bounce" },
            },
        },
        interactivity: {
            events: {
                onHover: { enable: true, mode: "grab" },
                resize: true,
            },
            modes: {
                grab: {
                    distance: 150,
                    links: { opacity: 0.24 },
                },
            },
        },
    });
}

async function fetchSiteData() {
    const response = await fetch("/api/site-data", {
        headers: { Accept: "application/json" },
    });

    if (!response.ok) {
        throw new Error("Unable to load portfolio data.");
    }

    return response.json();
}

function escapeHtml(value = "") {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function truncateText(value = "", maxLength = 220) {
    const normalized = String(value).replace(/\s+/g, " ").trim();
    if (normalized.length <= maxLength) {
        return normalized;
    }
    return `${normalized.slice(0, maxLength).trimEnd()}...`;
}

function titleForPage(page) {
    const name = appState.data?.contact?.name || "Portfolio";
    return `${name} | ${titles[page] || "Portfolio"}`;
}

function setNavState(open) {
    appState.navOpen = open;
    document.body.classList.toggle("nav-open", open);
    if (navPanel) {
        navPanel.classList.toggle("is-open", open);
    }
    if (navToggle) {
        navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    }
}

function showProgress() {
    if (progressBar) {
        progressBar.hidden = false;
        progressBar.classList.add("is-visible");
    }
}

function hideProgress() {
    if (progressBar) {
        progressBar.classList.remove("is-visible");
        window.setTimeout(() => {
            progressBar.hidden = true;
        }, 220);
    }
}

function updateNav(pathname) {
    document.querySelectorAll("[data-route]").forEach((link) => {
        link.classList.toggle("active", link.getAttribute("data-route") === pathname);
    });
}

function navigateTo(pathname, replace = false) {
    const url = routes[pathname] ? pathname : "/";
    if (!replace && url === window.location.pathname) {
        setNavState(false);
        renderRoute();
        return;
    }

    if (replace) {
        history.replaceState({}, "", url);
    } else {
        history.pushState({}, "", url);
    }
    setNavState(false);
    renderRoute();
}

function sectionHeader(title, copy, kicker = "Portfolio") {
    return `
        <header class="section-header">
            <div>
                <div class="eyebrow">${escapeHtml(kicker)}</div>
                <h1 class="page-title">${escapeHtml(title)}</h1>
            </div>
            <p>${escapeHtml(copy)}</p>
        </header>
    `;
}

function countSkills(skills = {}) {
    return Object.values(skills).reduce((count, items) => count + items.length, 0);
}

function safeProjects() {
    return appState.data?.sections?.projects || [];
}

function getFeaturedProject() {
    const projects = safeProjects();
    return projects.length ? projects[0] : null;
}

function getSupportProjects() {
    return safeProjects().slice(1);
}

function metricCard(label, value, note) {
    return `
        <article class="metric-card">
            <div class="metric-label">${escapeHtml(label)}</div>
            <div class="metric-value">${escapeHtml(String(value))}</div>
            <div class="metric-note">${escapeHtml(note)}</div>
        </article>
    `;
}

function detailList(items = []) {
    if (!items.length) {
        return `<p class="muted">Details will appear here.</p>`;
    }
    return `<ul class="detail-list">${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function renderHome(data) {
    const { contact, profile, sections, meta } = data;
    const currentExperience = sections.experiences[0] || {};
    const featuredProject = getFeaturedProject();
    const supportProjects = getSupportProjects().slice(0, 3);
    const metrics = [
        metricCard("Years building", "1+", "Applied AI, Python, and delivery-focused backend work."),
        metricCard("Projects", sections.projects.length, "Proof of implementation across product and engineering work."),
        metricCard("Certifications", sections.certifications.length, "Structured upskilling across AI, security, and web."),
        metricCard("Skill signals", countSkills(sections.skills), "Languages, frameworks, cloud, and analysis tooling."),
    ].join("");

    return `
        <section class="view home-view">
            <section class="hero-stage panel panel-hero">
                <div class="hero-copy">
                    <div class="eyebrow">AI engineering portfolio</div>
                    <h1 class="hero-title">Building practical AI systems, Python backends, and recruiter-readable proof.</h1>
                    <p class="hero-subtitle">${escapeHtml(profile)}</p>
                    <div class="hero-meta-row">
                        <div class="meta-pill">
                            <span class="meta-pill-label">Current role</span>
                            <strong>${escapeHtml(currentExperience.role || "AI Engineer")}</strong>
                        </div>
                        <div class="meta-pill">
                            <span class="meta-pill-label">Based in</span>
                            <strong>${escapeHtml(contact.location || "India")}</strong>
                        </div>
                    </div>
                    <div class="hero-actions">
                        <a class="button button-primary" href="/projects" data-link><i class="bi bi-stars"></i> Explore Projects</a>
                        <a class="button button-secondary" href="${escapeHtml(meta.resume_url)}"><i class="bi bi-download"></i> Download Resume</a>
                        <a class="button button-tertiary" href="/contact" data-link><i class="bi bi-arrow-up-right"></i> Contact</a>
                    </div>
                </div>
                <aside class="hero-proof-rail">
                    <div class="proof-chip">Recruiter-first structure</div>
                    <h2>What should stand out immediately</h2>
                    <p class="muted">Engineering credibility first, project proof second, personal story after the proof is established.</p>
                    <div class="signal-stack">
                        <div class="signal-card">
                            <span>Role focus</span>
                            <strong>${escapeHtml(currentExperience.role || "AI Engineer")}</strong>
                        </div>
                        <div class="signal-card">
                            <span>Company</span>
                            <strong>${escapeHtml(currentExperience.company || "Open to build")}</strong>
                        </div>
                        <div class="signal-card">
                            <span>Content mode</span>
                            <strong>${meta.source.database ? "Database-backed" : "JSON fallback"}</strong>
                        </div>
                    </div>
                </aside>
            </section>

            <section class="proof-strip">
                ${metrics}
            </section>

            <section class="editorial-grid">
                <article class="feature-panel panel panel-featured-project">
                    <div class="section-intro">
                        <div class="eyebrow">Featured work</div>
                        <h2>One project should carry the narrative weight.</h2>
                    </div>
                    ${featuredProject ? `
                        <div class="featured-project-layout">
                            <div>
                                 <div class="meta-line">Highlighted project</div>
                                 <h3>${escapeHtml(featuredProject.title)}</h3>
                                 ${detailList(featuredProject.highlights)}
                             </div>
                            <div class="featured-project-side">
                                <div class="project-side-card">
                                    <span>Primary proof</span>
                                    <strong>Implementation depth</strong>
                                    <p>${escapeHtml(featuredProject.link ? "Includes an external project link for direct review." : "Focused on delivery details and technical outcomes.")}</p>
                                    ${featuredProject.link ? `<a class="button button-secondary" href="${escapeHtml(featuredProject.link)}" target="_blank" rel="noopener noreferrer">Open Project</a>` : `<a class="button button-secondary" href="/projects" data-link>View Projects Route</a>`}
                                </div>
                            </div>
                        </div>
                    ` : `<div class="empty-card">Add projects to unlock the featured project section.</div>`}
                </article>

                <aside class="support-column">
                    <article class="panel support-panel">
                        <div class="eyebrow">Selected proof</div>
                        <h3>Current experience</h3>
                        <p class="muted">${escapeHtml(currentExperience.company || "Experience will appear here.")}</p>
                        <p class="support-lede">${escapeHtml(currentExperience.duration || "")}</p>
                        ${detailList((currentExperience.responsibilities || []).slice(0, 3))}
                    </article>
                    <article class="panel support-panel">
                        <div class="eyebrow">Contact path</div>
                        <h3>Available for technical conversations</h3>
                        <p class="muted">${escapeHtml(contact.email)}<br>${escapeHtml(contact.phone)}</p>
                        <div class="inline-actions">
                            <a class="button button-secondary" href="mailto:${escapeHtml(contact.email)}">Email</a>
                            <a class="button button-tertiary" href="https://${escapeHtml(contact.linkedin)}" target="_blank" rel="noopener noreferrer">LinkedIn</a>
                        </div>
                    </article>
                </aside>
            </section>

            <section class="support-projects-section">
                <div class="section-intro section-intro-slim">
                    <div class="eyebrow">Supporting projects</div>
                    <h2>Additional work that recruiters can scan quickly.</h2>
                </div>
                <div class="support-project-grid">
                    ${supportProjects.length
                        ? supportProjects.map((project) => `
                            <article class="project-mini-card">
                                <div class="meta-line">Project</div>
                                <h3>${escapeHtml(project.title)}</h3>
                                ${project.link ? `<a class="project-link" href="${escapeHtml(project.link)}" target="_blank" rel="noopener noreferrer">Open project</a>` : ""}
                            </article>
                        `).join("")
                        : `<div class="empty-card">Supporting projects will appear here once they are added.</div>`}
                </div>
            </section>
        </section>
    `;
}

function renderAbout(data) {
    const achievements = data.sections.achievements || [];
    const contact = data.contact || {};
    return `
        <section class="view">
            ${sectionHeader("About", "A clear technical profile: what you build, how you work, and why the portfolio is structured around proof.", "Profile")}
            <div class="editorial-grid editorial-grid-balanced">
                <article class="feature-panel panel">
                    <div class="meta-line">Professional summary</div>
                    <h2 class="section-title">Focused on practical delivery over generic claims.</h2>
                    <p class="lead-copy">${escapeHtml(data.profile)}</p>
                </article>
                <aside class="support-column">
                    <article class="panel support-panel">
                        <div class="eyebrow">Signals</div>
                        <h3>Working profile</h3>
                        <div class="support-pair"><span>Location</span><strong>${escapeHtml(contact.location || "Not listed")}</strong></div>
                        <div class="support-pair"><span>Email</span><strong>${escapeHtml(contact.email || "Not listed")}</strong></div>
                        <div class="support-pair"><span>LinkedIn</span><strong>${escapeHtml(contact.linkedin || "Not listed")}</strong></div>
                    </article>
                </aside>
            </div>
            <section class="panel list-panel">
                <div class="section-intro section-intro-slim">
                    <div class="eyebrow">Achievements</div>
                    <h2>Signals outside the day-to-day role.</h2>
                </div>
                <div class="achievement-grid">
                    ${achievements.length ? achievements.map((item) => `<div class="achievement-item">${escapeHtml(item)}</div>`).join("") : `<div class="empty-card">Achievements will appear here.</div>`}
                </div>
            </section>
        </section>
    `;
}

function renderEducation(data) {
    const items = data.sections.educations || [];
    return `
        <section class="view">
            ${sectionHeader("Education", "Academic background ordered to keep the strongest credential first and older education secondary.", "Foundation")}
            <div class="education-stack">
                ${items.map((item, index) => `
                    <article class="education-card ${index === 0 ? "education-card-primary" : ""}">
                        <div class="education-year">${escapeHtml(String(item.passing_year || "Year not listed"))}</div>
                        <div class="education-copy">
                            <h3>${escapeHtml(item.degree)}</h3>
                            <p class="muted">${escapeHtml(item.institute)}</p>
                            <div class="education-score">Score / CGPA: ${escapeHtml(String(item.cgpa || "N/A"))}</div>
                        </div>
                    </article>
                `).join("")}
            </div>
        </section>
    `;
}

function renderSkills(data) {
    const skills = data.sections.skills || {};
    const groups = Object.entries(skills);
    return `
        <section class="view">
            ${sectionHeader("Skills", "Capabilities grouped by actual delivery value: backend, ML, data work, and frontend support.", "Toolkit")}
            <div class="skill-band-grid">
                ${groups.map(([category, items], index) => `
                    <article class="skill-band ${index === 0 ? "skill-band-featured" : ""}">
                        <div class="meta-line">${escapeHtml(category.replaceAll("_", " "))}</div>
                        <h3>${escapeHtml(category.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase()))}</h3>
                        <div class="skill-cloud">
                            ${items.map((item) => `<span class="skill-pill">${escapeHtml(item)}</span>`).join("")}
                        </div>
                    </article>
                `).join("")}
            </div>
        </section>
    `;
}

function renderExperience(data) {
    const items = data.sections.experiences || [];
    const lead = items[0] || null;
    const rest = items.slice(1);
    return `
        <section class="view">
            ${sectionHeader("Experience", "Work presented around implementation signal, tooling depth, and practical contribution.", "Career")}
            ${lead ? `
                <section class="panel experience-lead">
                    <div class="experience-lead-top">
                        <div>
                            <div class="eyebrow">Current / lead role</div>
                            <h2>${escapeHtml(lead.role)}</h2>
                            <p class="muted">${escapeHtml(lead.company)}${lead.location ? `, ${escapeHtml(lead.location)}` : ""}</p>
                        </div>
                        <div class="experience-duration">${escapeHtml(lead.duration || "Duration not listed")}</div>
                    </div>
                    ${detailList(lead.responsibilities || [])}
                </section>
            ` : `<div class="empty-card">Experience will appear here.</div>`}
            ${rest.length ? `
                <div class="timeline compact-timeline">
                    ${rest.map((item) => `
                        <article class="timeline-card">
                            <div class="meta-line">${escapeHtml(item.duration || "Duration not listed")}</div>
                            <h3>${escapeHtml(item.role)}</h3>
                            <p class="muted">${escapeHtml(item.company)}${item.location ? `, ${escapeHtml(item.location)}` : ""}</p>
                            ${detailList((item.responsibilities || []).slice(0, 3))}
                        </article>
                    `).join("")}
                </div>
            ` : ""}
        </section>
    `;
}

function renderProjects(data) {
    const items = data.sections.projects || [];
    if (!items.length) {
        return `
            <section class="view">
                ${sectionHeader("Projects", "Featured project proof first, then supporting work that can be scanned quickly.", "Builds")}
                <div class="empty-card">Projects will appear here once they are added.</div>
            </section>
        `;
    }

    const featured = items[0];
    const supporting = items.slice(1);

    return `
        <section class="view">
            ${sectionHeader("Projects", "A proof-first project presentation with one primary story and supporting evidence beneath it.", "Builds")}
            <section class="panel featured-project-stage">
                <div class="featured-project-copy">
                    <div class="eyebrow">Featured project</div>
                    <h2>${escapeHtml(featured.title)}</h2>
                    ${detailList((featured.highlights || []).slice(0, 4))}
                </div>
                <aside class="featured-project-summary">
                    <div class="project-side-card">
                        <span>Role of this section</span>
                        <strong>Primary proof artifact</strong>
                        <p>${escapeHtml(featured.link ? "Includes an external link for deeper review." : "Focused on implementation highlights and delivery signal.")}</p>
                        ${featured.link ? `<a class="button button-secondary" href="${escapeHtml(featured.link)}" target="_blank" rel="noopener noreferrer">Open Project</a>` : `<a class="button button-secondary" href="/contact" data-link>Discuss the work</a>`}
                    </div>
                </aside>
            </section>

            <section class="support-projects-section">
                <div class="section-intro section-intro-slim">
                    <div class="eyebrow">Supporting work</div>
                    <h2>Additional projects that are easy to scan.</h2>
                </div>
                <div class="support-project-grid">
                    ${supporting.length ? supporting.map((item) => `
                        <article class="project-mini-card">
                            <div class="meta-line">Project</div>
                            <h3>${escapeHtml(item.title)}</h3>
                            ${item.link ? `<a class="project-link" href="${escapeHtml(item.link)}" target="_blank" rel="noopener noreferrer">Open project</a>` : ""}
                        </article>
                    `).join("") : `<div class="empty-card">Add more projects to populate the supporting grid.</div>`}
                </div>
            </section>
        </section>
    `;
}

function renderCertifications(data) {
    const items = data.sections.certifications || [];
    const safeIndex = Math.min(appState.activeCertIndex, Math.max(items.length - 1, 0));
    appState.activeCertIndex = safeIndex;
    const activeItem = items[safeIndex] || null;

    return `
        <section class="view">
            ${sectionHeader("Certifications", "Selected credentials that strengthen the AI, backend, data, and engineering story of the portfolio.", "Credentials")}
            <div class="cert-grid cert-grid-upgraded">
                <div class="cert-list">
                    ${items.map((item, index) => `
                        <article class="cert-card ${index === appState.activeCertIndex ? "is-active" : ""}" data-cert-index="${index}">
                            <div class="meta-line">${escapeHtml(item.year || "Credential")}</div>
                            <h3>${escapeHtml(item.title)}</h3>
                            <p class="muted">${escapeHtml(item.organization || "Organization not listed")}</p>
                        </article>
                    `).join("") || `<div class="empty-card">Certifications will appear here once they are added.</div>`}
                </div>
                <aside class="cert-preview">
                    ${activeItem?.image_url
                        ? `
                            <div class="cert-preview-frame">
                                <div class="meta-line" data-cert-year>${escapeHtml(activeItem.year || "Credential")}</div>
                                <h3 data-cert-title>${escapeHtml(activeItem.title)}</h3>
                                <p class="muted" data-cert-org>${escapeHtml(activeItem.organization || "Organization not listed")}</p>
                                <img data-cert-image src="${escapeHtml(activeItem.image_url)}" alt="${escapeHtml(activeItem.title)}">
                            </div>
                        `
                        : `
                            <div class="empty-card" data-cert-empty>
                                Select a certificate with an uploaded image to preview it here.
                            </div>
                        `}
                </aside>
            </div>
        </section>
    `;
}

function updateCertificationSelection(index) {
    const items = appState.data?.sections?.certifications || [];
    if (!items.length) {
        return;
    }

    const safeIndex = Math.min(Math.max(index, 0), items.length - 1);
    const activeItem = items[safeIndex];
    const preview = document.querySelector(".cert-preview");
    const image = document.querySelector("[data-cert-image]");
    const title = document.querySelector("[data-cert-title]");
    const org = document.querySelector("[data-cert-org]");
    const year = document.querySelector("[data-cert-year]");

    appState.activeCertIndex = safeIndex;

    document.querySelectorAll("[data-cert-index]").forEach((card) => {
        const isActive = Number(card.getAttribute("data-cert-index")) === safeIndex;
        card.classList.toggle("is-active", isActive);
    });

    if (!preview) {
        return;
    }

    if (activeItem?.image_url && image && title && org && year) {
        image.src = activeItem.image_url;
        image.alt = activeItem.title || "Certificate preview";
        title.textContent = activeItem.title || "Certificate";
        org.textContent = activeItem.organization || "Organization not listed";
        year.textContent = activeItem.year || "Credential";
        return;
    }

    preview.innerHTML = activeItem?.image_url
        ? `
            <div class="cert-preview-frame">
                <div class="meta-line" data-cert-year>${escapeHtml(activeItem.year || "Credential")}</div>
                <h3 data-cert-title>${escapeHtml(activeItem.title)}</h3>
                <p class="muted" data-cert-org>${escapeHtml(activeItem.organization || "Organization not listed")}</p>
                <img data-cert-image src="${escapeHtml(activeItem.image_url)}" alt="${escapeHtml(activeItem.title)}">
            </div>
        `
        : `
            <div class="empty-card" data-cert-empty>
                Select a certificate with an uploaded image to preview it here.
            </div>
        `;
}

function renderContact(data) {
    const contact = data.contact || {};
    return `
        <section class="view">
            ${sectionHeader("Contact", "Direct contact paths for roles, collaborations, and technical conversations after reviewing the work.", "Connect")}
            <section class="panel contact-stage">
                <div class="contact-stage-copy">
                    <div class="eyebrow">Available for AI and backend roles</div>
                    <h2>Review the work, then use the fastest path to continue the conversation.</h2>
                    <p class="lead-copy">Best suited for outreach around AI engineering, Python backend work, ML-focused projects, and technical collaboration.</p>
                </div>
                <div class="contact-card-grid contact-card-grid-wide">
                    <article class="contact-card contact-card-strong">
                        <i class="bi bi-envelope"></i>
                        <h3>Email</h3>
                        <p class="muted">${escapeHtml(contact.email)}</p>
                        <a class="button button-primary" href="mailto:${escapeHtml(contact.email)}">Write an email</a>
                    </article>
                    <article class="contact-card">
                        <i class="bi bi-telephone"></i>
                        <h3>Phone</h3>
                        <p class="muted">${escapeHtml(contact.phone)}</p>
                        <a class="button button-secondary" href="tel:${escapeHtml(contact.phone)}">Call directly</a>
                    </article>
                    <article class="contact-card">
                        <i class="bi bi-linkedin"></i>
                        <h3>LinkedIn</h3>
                        <p class="muted">${escapeHtml(contact.linkedin)}</p>
                        <a class="button button-secondary" href="https://${escapeHtml(contact.linkedin)}" target="_blank" rel="noopener noreferrer">Open LinkedIn</a>
                    </article>
                </div>
            </section>
        </section>
    `;
}

function renderView(page) {
    switch (page) {
        case "about":
            return renderAbout(appState.data);
        case "education":
            return renderEducation(appState.data);
        case "skills":
            return renderSkills(appState.data);
        case "experience":
            return renderExperience(appState.data);
        case "projects":
            return renderProjects(appState.data);
        case "certifications":
            return renderCertifications(appState.data);
        case "contact":
            return renderContact(appState.data);
        case "home":
        default:
            return renderHome(appState.data);
    }
}

function attachCertHandlers() {
    document.querySelectorAll("[data-cert-index]").forEach((card) => {
        card.addEventListener("click", () => {
            updateCertificationSelection(Number(card.getAttribute("data-cert-index")) || 0);
        });
    });
}

function cycleRoleLine() {
    const line = document.getElementById("role-line");
    if (!line) {
        if (appState.roleIntervalId) {
            clearInterval(appState.roleIntervalId);
            appState.roleIntervalId = null;
        }
        return;
    }

    const roles = ["AI Engineer", "Python Developer", "ML Builder", "Backend Problem Solver"];
    let index = 0;
    if (appState.roleIntervalId) {
        clearInterval(appState.roleIntervalId);
    }
    appState.roleIntervalId = setInterval(() => {
        index = (index + 1) % roles.length;
        line.textContent = `${roles[index]} with delivery-first execution`;
    }, 2600);
}

function renderRoute() {
    const pathname = routes[window.location.pathname] ? window.location.pathname : "/";
    const page = routes[pathname] || "home";
    updateNav(pathname);
    document.title = titleForPage(page);
    appRoot.innerHTML = renderView(page);
    appRoot.dataset.route = page;
    attachCertHandlers();
    cycleRoleLine();
    window.setTimeout(() => hideProgress(), 90);
}

function handleLinkClick(event) {
    const anchor = event.target.closest("[data-link]");
    if (!anchor) {
        return;
    }

    const href = anchor.getAttribute("href");
    if (!href || href.startsWith("http")) {
        return;
    }

    event.preventDefault();
    navigateTo(href);
}

async function bootstrap() {
    initParticles();
    document.addEventListener("click", handleLinkClick);
    window.addEventListener("popstate", () => {
        setNavState(false);
        renderRoute();
    });

    if (navToggle) {
        navToggle.addEventListener("click", () => {
            setNavState(!appState.navOpen);
        });
    }

    try {
        showProgress();
        appState.data = await fetchSiteData();
        renderRoute();
    } catch (error) {
        hideProgress();
        appRoot.innerHTML = `<section class="empty-card">${escapeHtml(error.message)}</section>`;
    }
}

bootstrap();
