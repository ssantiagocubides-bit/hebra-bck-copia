let tasks = [
    { id: 831, title: "Mantenimiento Telar A", desc: "Se realizó ajuste de tensión y lubricación de engranajes.", status: "finalizado", prio: "media", tag: "Mantenimiento", date: "Hoy, 09:15 AM", assignee: "Santiago Cano" },
    { id: 794, title: "Falla Eléctrica Sensor", desc: "Sensor óptico intermitente detiene la marcha.", status: "proceso", prio: "alta", tag: "Eléctrico", date: "Ayer, 03:40 PM", assignee: "Santiago Cano" },
    { id: 720, title: "Repuesto Agotado", desc: "Sin stock de materia prima en bodega central.", status: "pendiente", prio: "baja", tag: "Materia Prima", date: "28 May, 10:22 AM", assignee: "Otro Operario" }
];

const taskModal = new bootstrap.Modal(document.getElementById('taskModal'));
let draggedCard = null;
let draggedTaskId = null;
let draggedHeight = 0;

function createCard(task) {
    const card = document.createElement('div');
    card.className = 'task-card p-3 rounded-3 text-white mb-2 shadow-sm';
    card.style.background = '#2C3E42';
    card.draggable = true;
    card.dataset.id = task.id;

    const priorityText = { alta: '🔴 Alta', media: '⚪ Media', baja: '🟢 Baja' };
    const priorityClass = { alta: 'rgba(239, 68, 68, 0.2)', media: 'rgba(251, 146, 60, 0.2)', baja: 'rgba(34, 197, 94, 0.2)' };
    const priorityColor = { alta: '#FCA5A5', media: '#FDBA74', baja: '#86EFAC' };

    card.innerHTML = `
        <div class="fw-semibold text-light mb-1" style="font-size: 0.95rem; word-break: break-word;">${escapeHtml(task.title)}</div>
        <div class="task-desc text-secondary mb-2 small">${escapeHtml(task.desc)}</div>
        <div class="d-flex justify-content-between align-items-start mb-2">
          <div class="d-flex flex-wrap gap-1">
            <span class="badge rounded-1" style="background: ${priorityClass[task.prio]}; color: ${priorityColor[task.prio]}; font-size: 0.7rem;">${priorityText[task.prio]}</span>
            ${task.tag ? `<span class="badge rounded-1 fw-normal" style="background: rgba(165, 201, 202, 0.15); color: #A5C9CA; font-size: 0.7rem;">${escapeHtml(task.tag)}</span>` : ''}
          </div>
        </div>
        <div class="d-flex justify-content-between align-items-center pt-2 border-top border-secondary border-opacity-10 small" style="color: #A5C9CA; font-size: 0.75rem;">
          <span><i class="bi bi-calendar3 me-1"></i>${escapeHtml(task.date)}</span>
          <span class="fw-bold px-2 py-1 rounded" style="background: rgba(165, 201, 202, 0.1);">#${task.id}</span>
        </div>
      `;

    card.addEventListener('dragstart', (e) => {
        draggedCard = card;
        draggedTaskId = task.id;
        draggedHeight = card.offsetHeight;
        setTimeout(() => card.classList.add('dragging'), 0);
        e.dataTransfer.effectAllowed = 'move';
    });

    card.addEventListener('dragend', () => {
        draggedCard = null;
        draggedTaskId = null;
        card.classList.remove('dragging');
        document.querySelectorAll('.drop-placeholder').forEach(p => p.remove());
        document.querySelectorAll('.drop-zone').forEach(z => z.classList.remove('drag-over'));
    });

    card.addEventListener('click', (e) => {
        if (e.target.closest('.badge') || e.target.closest('.rounded')) return;
        openEditModal(task.id);
    });

    return card;
}

function setupDropZones() {
    document.querySelectorAll('.drop-zone').forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.closest('.kanban-column').classList.add('drag-over');

            const existing = zone.querySelector('.drop-placeholder');
            if (!existing) {
                const placeholder = document.createElement('div');
                placeholder.className = 'drop-placeholder';
                placeholder.style.height = `${draggedHeight}px`;
                zone.appendChild(placeholder);
            }
        });

        zone.addEventListener('dragleave', (e) => {
            if (!zone.contains(e.relatedTarget) && !zone.closest('.kanban-column').contains(e.relatedTarget)) {
                zone.closest('.kanban-column').classList.remove('drag-over');
                zone.querySelector('.drop-placeholder')?.remove();
            }
        });

        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.closest('.kanban-column').classList.remove('drag-over');
            zone.querySelector('.drop-placeholder')?.remove();

            if (!draggedTaskId) return;

            const newStatus = zone.dataset.status;
            const task = tasks.find(t => t.id == draggedTaskId);

            if (task && task.status !== newStatus) {
                task.status = newStatus;
                renderAll();
            }
        });
    });
}

function renderAll() {
    const lists = {
        pendiente: document.getElementById('list-pendiente'),
        proceso: document.getElementById('list-proceso'),
        finalizado: document.getElementById('list-finalizado')
    };

    const historyContainer = document.getElementById('historyItemsContainer');
    const assignedContainer = document.getElementById('assignedItemsContainer');

    Object.values(lists).forEach(l => { if (l) l.innerHTML = ''; });
    if (historyContainer) {
        historyContainer.innerHTML = '';
    }
    if (assignedContainer) assignedContainer.innerHTML = '';

    let counts = { pendiente: 0, proceso: 0, finalizado: 0 };
    const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
    const priorityFilter = document.getElementById('filterPrio')?.value || '';

    const filteredTasks = tasks.filter(task => {
        const matchSearch = task.title.toLowerCase().includes(searchTerm) ||
            task.desc.toLowerCase().includes(searchTerm) ||
            task.tag.toLowerCase().includes(searchTerm);
        const matchPriority = !priorityFilter || task.prio === priorityFilter;
        return matchSearch && matchPriority;
    });

    filteredTasks.forEach(task => {
        counts[task.status]++;
        const card = createCard(task);
        if (lists[task.status]) lists[task.status].appendChild(card);
    });

    tasks.forEach(task => {
        if (task.isReport && historyContainer) {
            const histClone = createCard(task);
            histClone.draggable = false;
            historyContainer.appendChild(histClone);
        }
        if (task.assignee === 'Santiago Cano' && assignedContainer) {
            const assignClone = createCard(task);
            assignClone.draggable = false;
            assignedContainer.appendChild(assignClone);
        }
    });

    if (historyContainer && historyContainer.children.length === 0) {
        historyContainer.innerHTML = `<div class="text-center text-secondary small py-3">No hay reportes generados aún.</div>`;
    }

    document.getElementById('totalTasks').innerText = tasks.length;
    ['pendiente', 'proceso', 'finalizado'].forEach(s => {
        const countEl = document.getElementById(`count-${s}`);
        if (countEl) countEl.innerText = counts[s];
        const statEl = document.getElementById(`stat${s.charAt(0).toUpperCase() + s.slice(1)}`);
        if (statEl) statEl.innerText = counts[s];
    });

    Object.entries(lists).forEach(([status, zone]) => {
        if (zone && zone.children.length === 0) {
            zone.innerHTML = `
            <div class="d-flex flex-column align-items-center justify-content-center text-center p-5 border border-dashed border-secondary border-opacity-25 rounded-3 m-2 flex-grow-1" style="color:#A5C9CA; opacity:0.5;">
              <i class="bi bi-inbox fs-1 mb-2 opacity-50"></i>
              <p class="mb-0 small">Sin tareas en ${status}</p>
            </div>`;
        }
    });

    setupDropZones();
}

document.getElementById('btnGenerateReport')?.addEventListener('click', () => {
    document.getElementById('taskId').value = '';
    document.getElementById('taskTitle').value = '';
    document.getElementById('taskDesc').value = '';
    document.getElementById('taskStatus').value = 'pendiente';
    document.getElementById('taskPrio').value = 'media';
    document.getElementById('taskTag').value = '';
    document.getElementById('taskAssignee').value = 'Santiago Cano';
    document.getElementById('modalTitle').innerText = 'Nuevo Reporte';
    document.getElementById('btnDelete').classList.add('d-none');
    taskModal.show();
});

function openEditModal(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    document.getElementById('taskId').value = task.id;
    document.getElementById('taskTitle').value = task.title;
    document.getElementById('taskDesc').value = task.desc;
    document.getElementById('taskStatus').value = task.status;
    document.getElementById('taskPrio').value = task.prio;
    document.getElementById('taskTag').value = task.tag;
    document.getElementById('taskAssignee').value = task.assignee || 'Santiago Cano';
    document.getElementById('modalTitle').innerText = `Editar Reporte #${task.id}`;
    document.getElementById('btnDelete').classList.remove('d-none');
    taskModal.show();
}

document.getElementById('btnSaveTask')?.addEventListener('click', () => {
    const id = document.getElementById('taskId').value;
    const title = document.getElementById('taskTitle').value.trim();
    const desc = document.getElementById('taskDesc').value.trim();
    const status = document.getElementById('taskStatus').value;
    const prio = document.getElementById('taskPrio').value;
    const tag = document.getElementById('taskTag').value.trim() || 'General';
    const assignee = document.getElementById('taskAssignee').value;

    if (!title || !desc) {
        alert('Por favor completa título y descripción');
        return;
    }

    if (id) {
        const task = tasks.find(t => t.id == id);
        if (task) {
            task.title = title; task.desc = desc; task.status = status;
            task.prio = prio; task.tag = tag; task.assignee = assignee;
        }
    } else {
        tasks.unshift({
            id: Math.floor(100 + Math.random() * 900),
            title, desc, status, prio, tag, assignee,
            date: 'Hoy, ' + new Date().toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' }),
            isReport: true
        });
    }
    taskModal.hide();
    renderAll();
});

document.getElementById('btnDelete')?.addEventListener('click', () => {
    const id = document.getElementById('taskId').value;
    if (id && confirm('¿Eliminar esta tarea?')) {
        tasks = tasks.filter(t => t.id != id);
        taskModal.hide();
        renderAll();
    }
});

document.getElementById('searchInput')?.addEventListener('input', renderAll);
document.getElementById('filterPrio')?.addEventListener('change', renderAll);

function escapeHtml(text) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return text.replace(/[&<>"']/g, m => map[m]);
}

document.addEventListener('DOMContentLoaded', renderAll);