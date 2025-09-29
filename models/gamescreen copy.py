import pygame, json
import sys
import os

# Agregar la raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

pygame.init()
from models.screen import Screen
from models.carrito import Carrito
from models.carretera import Carretera
from controller.grafico_avl import draw_avl
from avl.avl import AVL  # Importación correcta

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)

def tree_height(node):
    if not node:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))

class GameScreen(Screen):
    def __init__(self, display, config, game, avl_tree=None):
        super().__init__(display, config)
        self.fuente = pygame.font.Font(None, 25)
        self.game = game
        
        # Carretera
        self.carretera = Carretera(config["carretera"]["sprite"], config["ventana"]["alto"], config["ventana"]["ancho"], self.config)
        limite_sup, limite_inf = self.carretera.obtener_limites()
        posicion_inicial_y = (limite_sup + limite_inf) // 2
        
        # 🔹 Inicializar árbol AVL con manejo robusto de errores
        print("🔧 Iniciando inicialización del árbol AVL...")
        self.avl_tree = None
        
        try:
            # Verificar que la clase AVL esté disponible
            print(f"🔍 Clase AVL disponible: {AVL}")
            
            if avl_tree is None:
                print("🌳 Creando nuevo árbol AVL...")
                
                # Crear instancia de AVL de forma segura
                try:
                    self.avl_tree = AVL()
                    print(f"✓ Árbol AVL creado exitosamente: {type(self.avl_tree)}")
                    print(f"✓ Árbol tiene atributo root: {hasattr(self.avl_tree, 'root')}")
                    if hasattr(self.avl_tree, 'root'):
                        print(f"✓ Estado inicial de root: {self.avl_tree.root}")
                except Exception as e:
                    print(f"❌ Error creando instancia AVL: {e}")
                    import traceback
                    traceback.print_exc()
                    return  # Salir si no se puede crear el árbol
                
                print(f"📊 Obstáculos disponibles: {len(self.carretera.obstacles)}")
                
                if len(self.carretera.obstacles) == 0:
                    print("⚠️ No hay obstáculos para insertar en el árbol")
                else:
                    # Insertar obstáculos uno por uno con manejo de errores
                    inserted_count = 0
                    for i, obstacle in enumerate(self.carretera.obstacles):
                        try:
                            # Asignar ID si no existe
                            if not hasattr(obstacle, 'id'):
                                obstacle.id = i
                            
                            # Verificar que el árbol sigue siendo válido antes de insertar
                            if self.avl_tree is None:
                                print(f"❌ El árbol se volvió None antes de insertar obstáculo {i+1}")
                                break
                                
                            self.avl_tree.insert(obstacle)
                            inserted_count += 1
                            
                            if i < 3:  # Debug para los primeros 3
                                print(f"✓ Obstáculo {i+1} insertado: {obstacle.tipo}")
                                
                        except Exception as e:
                            print(f"❌ Error insertando obstáculo {i+1}: {e}")
                            # No hacer traceback para cada error, solo el primero
                            if i == 0:
                                import traceback
                                traceback.print_exc()
                    
                    print(f"🌳 Proceso completado. Obstáculos insertados: {inserted_count}")
                    
                    # Verificación final del estado del árbol
                    if self.avl_tree is not None:
                        try:
                            has_root = hasattr(self.avl_tree, 'root') and self.avl_tree.root is not None
                            print(f"🌳 Árbol tiene raíz: {has_root}")
                            if has_root:
                                inorder_count = len(self.avl_tree.inorder())
                                print(f"🌳 Nodos verificados en inorder: {inorder_count}")
                        except Exception as e:
                            print(f"❌ Error verificando estado final: {e}")
                    else:
                        print("🚨 PROBLEMA: El árbol es None después del proceso")
                        
            else:
                self.avl_tree = avl_tree
                print(f"🌳 Árbol AVL reutilizado")
                
        except Exception as e:
            print(f"❌ ERROR CRÍTICO en inicialización: {e}")
            import traceback
            traceback.print_exc()
            self.avl_tree = None
            
        # Estado final
        final_state = "válido" if self.avl_tree is not None else "None"
        print(f"🔍 Estado final del árbol: {final_state}")
        print("🔧 Inicialización completada.\n")

        # Jugador
        imagenes = [
            self.escalarImagen(pygame.image.load(config["carrito"]["colorDefault"])),
            self.escalarImagen(pygame.image.load(config["carrito"]["colorSalto"]))
        ]
        self.jugador = Carrito(30, posicion_inicial_y, imagenes, self.config)

        # Inputs
        zona_inputs_y = config["ventana"]["alto"] - 250
        self.input_rects = [pygame.Rect(150, zona_inputs_y + i*50 + 20, 100, 32) for i in range(4)]
        self.labels = ["Distancia (m):", "Salto (m):", "Velocidad (m):", "(ms):"]
        self.input_texts = [""]*4
        self.active_input = None

        # Movimiento
        self.moverArriba = False
        self.moverAbajo = False
        self.salto = False

    def escalarImagen(self, imagen, scale=None):
        if scale is None:
            scale = self.config["carrito"]["escala"]
        return pygame.transform.scale(imagen, (int(imagen.get_width()*scale), int(imagen.get_height()*scale)))

    # -------------------- Manejo de eventos --------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active_input = None
            for i, rect in enumerate(self.input_rects):
                if rect.collidepoint(event.pos):
                    self.active_input = i
                    break

        elif event.type == pygame.KEYDOWN:
            if self.active_input is not None:
                if event.key == pygame.K_BACKSPACE:
                    self.input_texts[self.active_input] = self.input_texts[self.active_input][:-1]
                elif event.key == pygame.K_RETURN:
                    try:
                        claves = [
                            ("carretera", "longitud"),
                            ("carrito", "salto"),
                            ("carrito", "avance_m"),
                            ("carrito", "avance_ms")
                        ]
                        clave_principal, subclave = claves[self.active_input]
                        if subclave == "longitud" and float(self.input_texts[self.active_input]) > 1000:
                            print("Longitud de carretera maxima: 1000m 🙈")
                            
                        self.config[clave_principal][subclave] = float(self.input_texts[self.active_input])

                        # Guardar en archivo
                        with open("config/config.json", "w") as f:
                            json.dump(self.config, f, indent=4)

                        # Recargar config desde archivo
                        with open("config/config.json", "r") as f:
                            self.config = json.load(f)
                            self.game.config = self.config
                            
                        # Cambiar la pantalla, pasando el árbol AVL actual
                        if pygame.get_init() and self.game.display:
                            self.game.set_screen(GameScreen(self.game.display, self.config, self.game, self.avl_tree))
                    except ValueError:
                        print("Ingrese un número válido")

                    self.input_texts[self.active_input] = ""

                else:
                    if event.unicode.isdigit() or event.unicode == ".":
                        self.input_texts[self.active_input] += event.unicode

            # Movimiento del jugador
            if event.key in (pygame.K_w, pygame.K_UP):
                self.moverArriba = True
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.moverAbajo = True
            if event.key == pygame.K_SPACE:
                self.salto = True

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_UP):
                self.moverArriba = False
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.moverAbajo = False
            if event.key == pygame.K_SPACE:
                self.salto = False

    # -------------------- Actualización de estado --------------------
    def update(self, dt_ms):
        self.carretera.actualizar(dt_ms)
        delta_y = 0
        if self.moverArriba:
            delta_y = -self.config["carrito"]["avance_m"]
        if self.moverAbajo:
            delta_y = self.config["carrito"]["avance_m"]

        limite_sup, limite_inf = self.carretera.obtener_limites()
        nueva_y = self.jugador.rect.y + delta_y
        nueva_y = max(limite_sup, min(nueva_y, limite_inf - self.jugador.rect.height))
        self.jugador.movimiento(nueva_y - self.jugador.rect.y, self.salto)
        
        # 💥 Colisiones con obstáculos
        for obst in self.carretera.obstacles:
            if self.jugador.rect.colliderect(obst.rect):
                if not obst.tocado:
                    obst.tocado = True
                    
                    # 🔹 ELIMINAR OBSTÁCULO DEL ÁRBOL AVL
                    print(f"🎯 Obstáculo tocado: {obst.tipo} en posición ({obst.posX}, {obst.posY})")
                    print(">>> Tipo de self.avl_tree en update:", type(self.avl_tree))
                    
                    if self.avl_tree:
                        try:
                            self.avl_tree.delete(obst)
                            remaining = len(self.avl_tree.inorder()) if self.avl_tree.root else 0
                            print(f"🌳 Árbol AVL actualizado. Nodos restantes: {remaining}")
                            print("Tipo de self.avl_tree:", type(self.avl_tree))
                            print("Tipo de obstáculo:", type(obst))
                            
                        except Exception as e:
                            print(f"❌ Error eliminando del árbol: {e}")
                    else:
                        print("⚠️ Árbol AVL no disponible para eliminar")
                    
                    if not self.jugador.esta_saltando:
                        if obst.tipo == "hueco":
                            print("❌ Caíste en un hueco.")
                        else:  # obstáculos sólidos
                            print(f"💥 Chocaste contra {obst.tipo}.")
                    
                        self.jugador.getDamage(int(obst.daño))
                        if self.jugador.dañado:
                            print("Carrito dañado 💀🚗")
                            self.game.running = False
                            
    # -------------------- Dibujado en pantalla --------------------
    def draw(self):
        self.display.fill(self.config["ventana"]["fondo"])
        self.carretera.dibujar(self.display)
        self.jugador.dibujar(self.display)
        self.barraSalud()

        # Inputs
        for i, rect in enumerate(self.input_rects):
            pygame.draw.rect(self.display, GRIS, rect)
            pygame.draw.rect(self.display, NEGRO, rect, 2)
            self.display.blit(self.fuente.render(self.labels[i], True, NEGRO), (20, rect.y + 5))
            self.display.blit(self.fuente.render(self.input_texts[i], True, NEGRO), (rect.x + 5, rect.y + 5))

        # 🔹 Árbol AVL escalable - con verificaciones de seguridad
        font = pygame.font.SysFont(None, 16)
        
        # Verificar que el árbol AVL existe y tiene raíz
        if self.avl_tree and hasattr(self.avl_tree, 'root') and self.avl_tree.root:
            try:
                h = tree_height(self.avl_tree.root)

                # Altura disponible debajo de la carretera
                available_height = self.config["ventana"]["alto"] * 0.4
                dy = max(50, int(available_height / h) if h > 0 else 50)

                # Anchura inicial
                dx = int(self.config["ventana"]["ancho"] * 0.12)

                # Radio de los nodos ajustado
                radius = max(10, int(40 - h * 2) if h > 0 else 20)

                draw_avl(self.display, self.avl_tree.root,
                        int(self.config["ventana"]["ancho"] * 0.7),
                        int(self.config["ventana"]["alto"] * 0.55),
                        dx, dy, font, radius)
            except Exception as e:
                print(f"Error dibujando árbol AVL: {e}")

        # 🔹 Información adicional del árbol - con verificaciones detalladas
        try:
            if self.avl_tree is not None:
                if hasattr(self.avl_tree, 'root') and self.avl_tree.root is not None:
                    try:
                        node_count = len(self.avl_tree.inorder())
                        tree_info = f"Nodos en árbol: {node_count}"
                    except:
                        tree_info = "Error contando nodos"
                else:
                    tree_info = "Árbol AVL: sin raíz"
            else:
                tree_info = "Árbol AVL: None"
        except Exception as e:
            tree_info = f"Error en árbol: {str(e)[:20]}"
            
        info_surface = self.fuente.render(tree_info, True, NEGRO)
        self.display.blit(info_surface, (10, self.config["ventana"]["alto"] - 30))

        pygame.display.flip()
        
    def barraSalud(self):
        pygame.draw.rect(self.display,(255,0,0),(10,10,self.jugador.energia_actual,20))