from pathlib import Path

from manim import *
from pydub import AudioSegment


ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "audio"
FONT = "Microsoft YaHei"
FORMULA_FONT = "Cambria Math"

CHAPTERS = [
    ("看不见的电场，怎样被测量？", "电场穿过一个面有多少？", "Φ_E = ∫ E · dA"),
    ("电通量：场穿过表面的多少", "只计算电场沿面积法线的分量", "Φ_E = ∫_S E · dA"),
    ("高斯定理的核心公式", "闭合面的净通量只取决于包围的净电荷", "∮_S E · dA = Q_enc / ε₀"),
    ("为什么点电荷适合用球面？", "球对称使球面上每点场强相同", "E · 4πr² = q / ε₀"),
    ("带电球壳与球形电荷分布", "内外分别选取高斯面，计算包围电荷", "E(r) = Q_enc(r) / (4π ε₀ r²)"),
    ("长直带电导线与圆柱高斯面", "同轴圆柱侧面有通量，端面没有", "E(r) = λ / (2π ε₀ r)"),
    ("无限带电平面与药盒高斯面", "穿过两端盖的总通量是 2EA", "E = σ / (2 ε₀)"),
    ("外部电荷与电场叠加", "外部电荷的进入与离开通量相互抵消", "Φ_E = Q_enc / ε₀"),
    ("导体静电平衡与电场屏蔽", "金属内部静电场为零，多余电荷在表面", "E_⊥ = σ / ε₀"),
    ("局部形式：散度定理的桥梁", "积分形式与每一点的局部规律等价", "∇ · E = ρ / ε₀"),
    ("与引力的类比，以及适用边界", "相似的数学结构，不同的场源与符号", "∮_S g · dA = −4π G M_enc"),
    ("总结：通量守恒与巧选高斯面", "理解通量、包围电荷与对称性", "∮_S E · dA = Q_enc / ε₀"),
]


class GaussLaw(Scene):
    def construct(self):
        self.camera.background_color = "#07111F"
        self.add(self.make_background())

        for index, (title, subtitle, equation) in enumerate(CHAPTERS, start=1):
            audio_path = AUDIO_DIR / ("chapter_%02d.mp3" % index)
            if not audio_path.exists():
                raise FileNotFoundError(
                    "Missing narration audio: %s. Run generate_voice.py first." % audio_path
                )
            duration = len(AudioSegment.from_file(audio_path)) / 1000.0
            self.show_chapter(index, title, subtitle, equation, duration)

    def make_background(self):
        lines = VGroup()
        for x in range(-8, 9):
            lines.add(Line([x, -4.5, 0], [x, 4.5, 0], stroke_color="#17304A", stroke_width=0.5))
        for y in range(-5, 6):
            lines.add(Line([-8.5, y, 0], [8.5, y, 0], stroke_color="#17304A", stroke_width=0.5))
        return lines.set_opacity(0.35)

    def show_chapter(self, index, title, subtitle, equation, duration):
        old = [mob for mob in self.mobjects if mob is not self.mobjects[0]]
        if old:
            self.remove(*old)

        header = Text(title, font=FONT, font_size=36, color="#F1F6FC")
        header.to_edge(UP, buff=0.38).to_edge(LEFT, buff=0.65)
        chapter_number = Text("%02d / 12" % index, font="Arial", font_size=19, color="#8BABC8")
        chapter_number.to_edge(UP, buff=0.48).to_edge(RIGHT, buff=0.65)
        sub = Text(subtitle, font=FONT, font_size=23, color="#A9C6E2")
        sub.next_to(header, DOWN, aligned_edge=LEFT, buff=0.18)
        formula = Text(
            equation,
            font=FORMULA_FONT,
            font_size=26 if index not in (3, 5, 11) else 22,
            color="#68D7FF",
            weight=MEDIUM,
        )
        formula.to_edge(DOWN, buff=0.38)
        rule = Line(LEFT * 6.95, RIGHT * 6.95, color="#27435F", stroke_width=1)
        rule.next_to(sub, DOWN, buff=0.22)
        diagram, path = self.make_diagram(index)
        diagram.move_to(ORIGIN + DOWN * 0.15)
        path.shift(DOWN * 0.15)

        self.play(
            FadeIn(header, shift=DOWN * 0.12),
            FadeIn(chapter_number),
            FadeIn(sub),
            Create(rule),
            Write(formula),
            run_time=2.0,
        )
        self.play(
            LaggedStart(*[FadeIn(mob, scale=0.9) for mob in diagram], lag_ratio=0.08),
            run_time=2.0,
        )

        marker = Dot(path.point_from_proportion(0), radius=0.085, color="#FFD166")
        marker.set_z_index(5)
        self.add(marker)
        self.play(
            MoveAlongPath(marker, path),
            run_time=max(0.1, duration - 4.0),
            rate_func=linear,
        )
        self.remove(marker)

    def make_diagram(self, index):
        methods = {
            1: self.diagram_flux_definition,
            2: self.diagram_tilted_surface,
            3: self.diagram_gauss_sphere,
            4: self.diagram_point_charge,
            5: self.diagram_spherical_shell,
            6: self.diagram_line_charge,
            7: self.diagram_sheet_charge,
            8: self.diagram_external_charge,
            9: self.diagram_conductor,
            10: self.diagram_divergence,
            11: self.diagram_gravity,
            12: self.diagram_applications,
        }
        return methods[index]()

    def diagram_flux_definition(self):
        surface = Rectangle(width=4.4, height=2.1, color="#68D7FF", stroke_width=3)
        surface.set_fill("#68D7FF", opacity=0.09).rotate(-0.15).shift(DOWN * 0.3)
        center = surface.get_center()
        normals = VGroup(*[
            Arrow(center + RIGHT * x, center + RIGHT * x + UP * 1.15, color="#FFD166", buff=0)
            for x in (-1.35, 0, 1.35)
        ])
        field = VGroup(*[
            Arrow(LEFT * 4.5 + UP * y, LEFT * 2.5 + UP * y, color="#FF6B6B", buff=0)
            for y in (-0.75, -0.15, 0.45, 1.05)
        ])
        label = Text("面元 dA", font=FONT, font_size=23, color="#68D7FF").next_to(surface, DOWN, buff=0.22)
        group = VGroup(surface, normals, field, label)
        return group, Line(LEFT * 4.5 + DOWN * 1.6, RIGHT * 4.5 + DOWN * 1.6)

    def diagram_tilted_surface(self):
        plane = Polygon(
            LEFT * 2.5 + DOWN * 0.75,
            RIGHT * 2.5 + DOWN * 0.05,
            RIGHT * 2.5 + UP * 0.75,
            LEFT * 2.5 + UP * 0.05,
            color="#68D7FF",
            stroke_width=3,
        ).set_fill("#68D7FF", opacity=0.1)
        center = Dot(ORIGIN, color="#FFD166", radius=0.07)
        normal = Arrow(ORIGIN, UP * 1.7 + LEFT * 1.7, color="#FFD166", buff=0)
        electric = Arrow(ORIGIN, RIGHT * 2.5, color="#FF6B6B", buff=0)
        angle = Arc(radius=0.7, start_angle=PI / 4, angle=PI / 4, color="#F1F6FC", stroke_width=2)
        theta = Text("θ", font=FORMULA_FONT, font_size=29, color="#F1F6FC").move_to(LEFT * 0.65 + UP * 0.35)
        label_n = Text("法线 n̂", font=FONT, font_size=21, color="#FFD166").next_to(normal.get_end(), UP, buff=0.12)
        label_e = Text("E", font=FORMULA_FONT, font_size=27, color="#FF6B6B").next_to(electric.get_end(), RIGHT, buff=0.12)
        group = VGroup(plane, center, normal, electric, angle, theta, label_n, label_e)
        return group, Line(LEFT * 4.3 + DOWN * 1.6, RIGHT * 4.3 + DOWN * 1.6)

    def diagram_gauss_sphere(self):
        sphere = Circle(radius=1.5, color="#68D7FF", stroke_width=3)
        sphere.set_fill("#68D7FF", opacity=0.07).shift(LEFT * 0.4)
        q = Dot(LEFT * 0.4, radius=0.2, color="#FF6B6B")
        plus = Text("+Q", font=FORMULA_FONT, font_size=24, color="#FF6B6B").next_to(q, UP, buff=0.12)
        rays = VGroup()
        for angle in np.linspace(0, TAU, 12, endpoint=False):
            unit = np.array([np.cos(angle), np.sin(angle), 0])
            rays.add(Arrow(LEFT * 0.4 + unit * 0.35, LEFT * 0.4 + unit * 2.35,
                           color="#FFD166", stroke_width=2.2, max_tip_length_to_length_ratio=0.12))
        label = Text("任意闭合高斯面", font=FONT, font_size=23, color="#68D7FF").next_to(sphere, DOWN, buff=0.3)
        group = VGroup(sphere, rays, q, plus, label)
        return group, Circle(radius=1.55).shift(LEFT * 0.4)

    def diagram_point_charge(self):
        q = Dot(LEFT * 0.4, radius=0.23, color="#FF6B6B")
        label_q = Text("+q", font=FORMULA_FONT, font_size=24, color="#FF6B6B").next_to(q, DOWN, buff=0.12)
        sphere = Circle(radius=1.8, color="#68D7FF", stroke_width=3).shift(LEFT * 0.4)
        field = VGroup()
        for angle in np.linspace(0, TAU, 8, endpoint=False):
            unit = np.array([np.cos(angle), np.sin(angle), 0])
            field.add(Arrow(LEFT * 0.4 + unit * 0.33, LEFT * 0.4 + unit * 2.55,
                            color="#FFD166", stroke_width=2.3))
        radius = Arrow(LEFT * 0.4, RIGHT * 1.4, color="#F1F6FC", buff=0.06)
        rlabel = Text("r", font=FORMULA_FONT, font_size=25, color="#F1F6FC").next_to(radius, DOWN, buff=0.1)
        caption = Text("球面上 E 大小相等且垂直于 dA", font=FONT, font_size=21, color="#A9C6E2").move_to(DOWN * 1.85)
        return VGroup(sphere, field, q, label_q, radius, rlabel, caption), Circle(radius=1.8).shift(LEFT * 0.4)

    def diagram_spherical_shell(self):
        inner = Circle(radius=0.85, color="#FF6B6B", stroke_width=2.5).shift(LEFT * 1.2)
        inner.set_fill("#FF6B6B", opacity=0.08)
        shell = Circle(radius=1.75, color="#68D7FF", stroke_width=3).shift(LEFT * 1.2)
        charge = VGroup(*[
            Dot(LEFT * 1.2 + np.array([np.cos(t), np.sin(t), 0]) * 1.25, radius=0.07, color="#FFD166")
            for t in np.linspace(0, TAU, 16, endpoint=False)
        ])
        outer = Circle(radius=2.25, color="#2CB67D", stroke_width=2, stroke_opacity=0.8).shift(LEFT * 1.2)
        qin = Text("r < R", font=FORMULA_FONT, font_size=22, color="#FF6B6B").move_to(RIGHT * 1.3 + UP * 0.65)
        qout = Text("r > R", font=FORMULA_FONT, font_size=22, color="#2CB67D").move_to(RIGHT * 1.3 + DOWN * 0.15)
        note = Text("内：包围电荷为零    外：包围总电荷 Q", font=FONT, font_size=20, color="#A9C6E2").move_to(DOWN * 1.75)
        return VGroup(shell, inner, outer, charge, qin, qout, note), Circle(radius=2.25).shift(LEFT * 1.2)

    def diagram_line_charge(self):
        wire = Line(LEFT * 0.3 + DOWN * 2.1, LEFT * 0.3 + UP * 2.1, color="#FF6B6B", stroke_width=9)
        wire_label = Text("λ", font=FORMULA_FONT, font_size=28, color="#FF6B6B").next_to(wire, LEFT, buff=0.2)
        cylinder = VGroup(
            Ellipse(width=3.0, height=0.72, color="#68D7FF", stroke_width=2.7).shift(UP * 1.3),
            Ellipse(width=3.0, height=0.72, color="#68D7FF", stroke_width=2.7).shift(DOWN * 1.3),
            Line(LEFT * 1.5 + UP * 1.3, LEFT * 1.5 + DOWN * 1.3, color="#68D7FF", stroke_width=2.7),
            Line(RIGHT * 1.5 + UP * 1.3, RIGHT * 1.5 + DOWN * 1.3, color="#68D7FF", stroke_width=2.7),
        )
        side_arrows = VGroup(*[
            Arrow(LEFT * 1.05 + UP * y, LEFT * 2.15 + UP * y, color="#FFD166", buff=0.08)
            for y in (-0.8, 0, 0.8)
        ])
        r = DoubleArrow(LEFT * 0.05, LEFT * 1.42, color="#F1F6FC", buff=0.04)
        rlabel = Text("r", font=FORMULA_FONT, font_size=23, color="#F1F6FC").next_to(r, DOWN, buff=0.08)
        return VGroup(cylinder, wire, wire_label, side_arrows, r, rlabel), Ellipse(width=3.0, height=0.72).shift(UP * 1.3)

    def diagram_sheet_charge(self):
        sheet = Rectangle(width=5.1, height=0.12, color="#FF6B6B", stroke_width=1).set_fill("#FF6B6B", opacity=0.85)
        gaussian = VGroup(
            Ellipse(width=2.0, height=0.52, color="#68D7FF", stroke_width=2.5).shift(UP * 1.25),
            Ellipse(width=2.0, height=0.52, color="#68D7FF", stroke_width=2.5).shift(DOWN * 1.25),
            Line(LEFT + UP * 1.25, LEFT + DOWN * 1.25, color="#68D7FF", stroke_width=2.5),
            Line(RIGHT + UP * 1.25, RIGHT + DOWN * 1.25, color="#68D7FF", stroke_width=2.5),
        )
        flux = VGroup(
            Arrow(UP * 0.5, UP * 2.4, color="#FFD166", buff=0),
            Arrow(DOWN * 0.5, DOWN * 2.4, color="#FFD166", buff=0),
        )
        sigma = Text("面电荷密度 σ", font=FONT, font_size=23, color="#FF6B6B").next_to(sheet, RIGHT, buff=0.35)
        captions = VGroup(
            Text("上盖通量 EA", font=FONT, font_size=20, color="#FFD166").move_to(RIGHT * 2.55 + UP * 1.2),
            Text("下盖通量 EA", font=FONT, font_size=20, color="#FFD166").move_to(RIGHT * 2.55 + DOWN * 1.2),
        )
        return VGroup(sheet, gaussian, flux, sigma, captions), Line(LEFT * 4.2 + DOWN * 1.75, RIGHT * 4.2 + DOWN * 1.75)

    def diagram_external_charge(self):
        surface = Circle(radius=1.6, color="#68D7FF", stroke_width=3).shift(LEFT * 0.8)
        surface.set_fill("#68D7FF", opacity=0.06)
        external = Dot(RIGHT * 2.8 + UP * 0.65, radius=0.2, color="#FF6B6B")
        label = Text("+q outside", font=FORMULA_FONT, font_size=22, color="#FF6B6B").next_to(external, UP, buff=0.12)
        enter = Arrow(RIGHT * 2.55 + DOWN * 0.65, RIGHT * 0.25 + DOWN * 0.65, color="#FFD166", stroke_width=2.5)
        leave = Arrow(LEFT * 0.25 + DOWN * 0.65, LEFT * 2.5 + DOWN * 0.65, color="#2CB67D", stroke_width=2.5)
        ins = Text("进入：负通量", font=FONT, font_size=19, color="#FFD166").next_to(enter, DOWN, buff=0.1)
        outs = Text("离开：正通量", font=FONT, font_size=19, color="#2CB67D").next_to(leave, DOWN, buff=0.1)
        group = VGroup(surface, external, label, enter, leave, ins, outs)
        return group, Circle(radius=1.6).shift(LEFT * 0.8)

    def diagram_conductor(self):
        conductor = RoundedRectangle(width=3.0, height=2.0, corner_radius=0.18)
        conductor.set_fill("#263E58", opacity=0.75).set_stroke("#829AB1", 2)
        conductor.move_to(LEFT * 1.3)
        charges = VGroup(*[
            Dot(LEFT * 1.3 + np.array([1.5 * np.cos(t), 0.92 * np.sin(t), 0]),
                radius=0.09, color="#FF6B6B")
            for t in np.linspace(0, TAU, 16, endpoint=False)
        ])
        zero = Text("E = 0", font=FORMULA_FONT, font_size=30, color="#68D7FF").move_to(LEFT * 1.3)
        gauss = Rectangle(width=1.45, height=0.95, color="#FFD166", stroke_width=2.5)
        gauss.set_fill("#FFD166", opacity=0.08).move_to(LEFT * 1.3)
        field = VGroup(*[
            Arrow(RIGHT * 0.55 + UP * y, RIGHT * 2.2 + UP * y, color="#2CB67D", buff=0.1)
            for y in (-0.7, 0, 0.7)
        ])
        outside = Text("导体外电场", font=FONT, font_size=21, color="#2CB67D").next_to(field, RIGHT, buff=0.1)
        return VGroup(conductor, charges, zero, gauss, field, outside), Circle(radius=1.95).shift(LEFT * 1.3)

    def diagram_divergence(self):
        cube = Cube(side_length=1.7, fill_opacity=0.12, fill_color="#68D7FF", stroke_color="#68D7FF")
        cube.shift(LEFT * 0.6)
        arrows = VGroup()
        center = LEFT * 0.6
        for direction in (UP, DOWN, LEFT, RIGHT):
            start = center + direction * 0.75
            end = center + direction * 2.0
            arrows.add(Arrow(start, end, color="#FFD166", buff=0))
        for point in (
            LEFT * 1.2 + UP * 1.2,
            LEFT * 0.1 + UP * 1.2,
            LEFT * 1.2 + DOWN * 0.1,
            LEFT * 0.1 + DOWN * 0.1,
        ):
            arrows.add(Arrow(point, point + RIGHT * 0.65 + UP * 0.55, color="#2CB67D", buff=0))
        rho = Text("ρ > 0", font=FORMULA_FONT, font_size=24, color="#FF6B6B").move_to(RIGHT * 2.45 + UP * 0.3)
        label = Text("局部净流出", font=FONT, font_size=22, color="#FFD166").next_to(rho, DOWN, buff=0.15)
        return VGroup(cube, arrows, rho, label), Line(LEFT * 4.2 + DOWN * 1.65, RIGHT * 4.2 + DOWN * 1.65)

    def diagram_gravity(self):
        mass = Circle(radius=0.52, color="#FF6B6B", stroke_width=2.5)
        mass.set_fill("#FF6B6B", opacity=0.2).move_to(LEFT * 0.45)
        mlabel = Text("M", font=FORMULA_FONT, font_size=26, color="#FF6B6B").move_to(mass)
        gaussian = Circle(radius=1.75, color="#68D7FF", stroke_width=2.5).shift(LEFT * 0.45)
        arrows = VGroup(*[
            Arrow(LEFT * 0.45 + np.array([np.cos(t), np.sin(t), 0]) * 1.15,
                  LEFT * 0.45 + np.array([np.cos(t), np.sin(t), 0]) * 0.48,
                  color="#FFD166", stroke_width=2.3)
            for t in np.linspace(0, TAU, 12, endpoint=False)
        ])
        note = Text("引力场线向内汇聚", font=FONT, font_size=22, color="#A9C6E2").move_to(RIGHT * 2.4 + UP * 0.25)
        g = Text("g", font=FORMULA_FONT, font_size=27, color="#FFD166").next_to(note, DOWN, buff=0.25)
        return VGroup(gaussian, arrows, mass, mlabel, note, g), Circle(radius=1.75).shift(LEFT * 0.45)

    def diagram_applications(self):
        sphere = Circle(radius=0.67, color="#68D7FF", stroke_width=2.5).set_fill("#68D7FF", opacity=0.12)
        sphere.move_to(LEFT * 4.2 + UP * 0.25)
        sphere_q = Dot(sphere.get_center(), radius=0.12, color="#FF6B6B")
        sphere_label = Text("球面", font=FONT, font_size=19, color="#A9C6E2").next_to(sphere, DOWN, buff=0.16)

        cylinder = VGroup(
            Ellipse(width=1.55, height=0.48, color="#2CB67D", stroke_width=2.5).shift(UP * 0.75),
            Ellipse(width=1.55, height=0.48, color="#2CB67D", stroke_width=2.5).shift(DOWN * 0.75),
            Line(LEFT * 0.78 + UP * 0.75, LEFT * 0.78 + DOWN * 0.75, color="#2CB67D", stroke_width=2.5),
            Line(RIGHT * 0.78 + UP * 0.75, RIGHT * 0.78 + DOWN * 0.75, color="#2CB67D", stroke_width=2.5),
        ).move_to(UP * 0.25)
        line = Line(cylinder.get_center() + UP * 0.5, cylinder.get_center() + DOWN * 0.5, color="#FF6B6B", stroke_width=5)
        cylinder_label = Text("圆柱", font=FONT, font_size=19, color="#A9C6E2").next_to(cylinder, DOWN, buff=0.16)

        sheet = Rectangle(width=1.75, height=0.1, color="#FF6B6B", stroke_width=1).set_fill("#FF6B6B", opacity=0.9)
        sheet.move_to(RIGHT * 3.55 + UP * 0.25)
        pillbox = VGroup(
            Ellipse(width=0.85, height=0.28, color="#FFD166", stroke_width=2.2).shift(UP * 0.72),
            Ellipse(width=0.85, height=0.28, color="#FFD166", stroke_width=2.2).shift(DOWN * 0.25),
            Line(LEFT * 0.43 + UP * 0.72, LEFT * 0.43 + DOWN * 0.25, color="#FFD166", stroke_width=2.2),
            Line(RIGHT * 0.43 + UP * 0.72, RIGHT * 0.43 + DOWN * 0.25, color="#FFD166", stroke_width=2.2),
        ).move_to(RIGHT * 3.55 + UP * 0.25)
        sheet_label = Text("药盒", font=FONT, font_size=19, color="#A9C6E2").next_to(pillbox, DOWN, buff=0.2)
        group = VGroup(sphere, sphere_q, sphere_label, cylinder, line, cylinder_label, sheet, pillbox, sheet_label)
        return group, Line(LEFT * 4.4 + DOWN * 1.65, RIGHT * 4.4 + DOWN * 1.65)


if __name__ == "__main__":
    print("Render with: py -3.10 render_video.py")
