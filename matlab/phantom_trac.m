mdl_phantomx

% Posiciones en coordenadas homogéneas
P_inicio = transl(200, -200, 200);  % Posición de espera
P_pick   = transl(200, -200, 20);  % Punto de recolección
P_lift   = transl(100, -100, 100);   % Levantar el objeto
P_place  = transl(200, 200, 20);   % Punto de colocación
P_final  = transl(200, 100, 200);   % Retorno a posición de espera

% Resolver cinemática inversa
q_inicio = px.ikine(P_inicio, qz, [1 1 1 0 0 0]);
q_pick   = px.ikine(P_pick, q_inicio, [1 1 1 0 0 0]);
q_lift   = px.ikine(P_lift, q_pick, [1 1 1 0 0 0]);
q_place  = px.ikine(P_place, q_lift, [1 1 1 0 0 0]);
q_final  = px.ikine(P_final, q_place, [1 1 1 0 0 0]);

% Generar trayectorias de interpolación
t = 0:0.05:3; % Tiempo de interpolación

q_trayectoria0 = jtraj(qz, q_inicio, t);
q_trayectoria1 = jtraj(q_inicio, q_pick, t);
q_trayectoria2 = jtraj(q_pick, q_lift, t);
q_trayectoria3 = jtraj(q_lift, q_place, t);
q_trayectoria4 = jtraj(q_place, q_final, t);
q_trayectoria5 = jtraj(q_final, qz, t);

% Unir todas las trayectorias
q_total = [q_trayectoria0; q_trayectoria1; q_trayectoria2; q_trayectoria3; q_trayectoria4; q_trayectoria5];

% Simular el movimiento del robot
h = figure;
view(140,20)
set(h, 'WindowState', 'maximized'); % Maximiza la ventana
px.plot(q_total);

