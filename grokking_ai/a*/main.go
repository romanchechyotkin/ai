package main

import (
	"fmt"
)

type Vertex struct {
	Name string
}

func NewVertex(name string) *Vertex {
	return &Vertex{
		Name: name,
	}
}

type Edge struct {
	Source      *Vertex
	Destination *Vertex
	Weight      int
}

func NewEdge(src, dst *Vertex, weight int) *Edge {
	return &Edge{
		Source:      src,
		Destination: dst,
		Weight:      weight,
	}
}

type Graph struct {
	Vertices []*Vertex
	Edges    []*Edge
}

func NewGraph(size uint) *Graph {
	return &Graph{
		Vertices: make([]*Vertex, 0, size),
		Edges:    make([]*Edge, 0, size*(size-1)),
	}
}

func (g *Graph) AddVertex(v *Vertex) *Vertex {
	g.Vertices = append(g.Vertices, v)
	return v
}

func (g *Graph) AddEdge(e *Edge) *Edge {
	g.Edges = append(g.Edges, e)
	return e
}

func (g *Graph) Info() {
	fmt.Printf("Vertices: %d\n", len(g.Vertices))
	fmt.Printf("Edges: %d\n", len(g.Edges))

	for _, e := range g.Edges {
		fmt.Printf("%s -> %s: %d\n", e.Source.Name, e.Destination.Name, e.Weight)
	}

	fmt.Println()
}

var moskow = NewVertex("Moskow")
var minsk = NewVertex("Minsk")
var prague = NewVertex("Prague")
var warsaw = NewVertex("Warsaw")
var london = NewVertex("London")
var madrid = NewVertex("Madrid")
var instanbul = NewVertex("Istanbul")

func main() {
	verteces := []*Vertex{minsk, moskow, prague, warsaw, london, madrid, instanbul}

	g := NewGraph(uint(len(verteces)))

	for _, v := range verteces {
		g.AddVertex(v)
	}

	edges := prepareEdges()
	for _, e := range edges {
		g.AddEdge(e)
	}

	g.Info()
}

func prepareEdges() []*Edge {
	e1 := NewEdge(minsk, moskow, 500)
	e2 := NewEdge(moskow, minsk, 500)

	e3 := NewEdge(moskow, instanbul, 1200)
	e4 := NewEdge(instanbul, moskow, 1200)

	e5 := NewEdge(london, madrid, 250)
	e6 := NewEdge(madrid, london, 250)

	e7 := NewEdge(minsk, warsaw, 400)
	e8 := NewEdge(warsaw, minsk, 400)

	e9 := NewEdge(instanbul, warsaw, 700)
	e10 := NewEdge(warsaw, instanbul, 700)

	e11 := NewEdge(london, prague, 450)
	e12 := NewEdge(prague, london, 450)

	e13 := NewEdge(warsaw, prague, 100)
	e14 := NewEdge(prague, warsaw, 100)

	return []*Edge{e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14}
}
