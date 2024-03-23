//
//  ContentView.swift
//  Airpods Control
//
//  Created by Siddharth Lakkoju on 3/20/24.
//

import SwiftUI
import CoreMotion
import SceneKit


// Tello Stuff
import CocoaAsyncSocket

struct ContentView: View {
    
    @StateObject private var viewModel = ViewModel()
    
    private let scene = SCNScene()
    private let cubeNode = SCNNode()
    
    
    var body: some View {
        
        VStack {
            
            SceneView(
                scene: scene,
                pointOfView: nil,
                options: [.autoenablesDefaultLighting],
                delegate: nil,
                technique: nil
            )
            .background(Color.black)
            .frame(width: 400, height: 400)
            .onAppear {
                setupScene()
            }
            .onChange(of: viewModel.cubeRotation) {
                cubeNode.eulerAngles = SCNVector3(viewModel.cubeRotation[0], viewModel.cubeRotation[1], -1*viewModel.cubeRotation[2])
            }
            .padding()
            
            Button("Take Off") {
                viewModel.takeOff()
            }
            .padding()
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(5)
            
            Button("Land") {
                viewModel.land()
            }
            .padding()
            .background(Color.red)
            .foregroundColor(.white)
            .cornerRadius(5)
            
            Text(viewModel.direction)
                .padding()
            
            Button("Emergency") {
                viewModel.emergency()
            }
        }
        .onAppear {
            viewModel.startMonitoring()
            viewModel.setupTello()
            
            print("Hello")
        }
        .onDisappear {
            viewModel.stopMonitoring()
        }
    }
    
    
    private func setupScene() {
        let cameraNode = SCNNode()
        cameraNode.camera = SCNCamera()
        cameraNode.position = SCNVector3(x: 0, y: 0, z: 15)
        scene.rootNode.addChildNode(cameraNode)
        let cubeGeometry = SCNBox(width: 3, height: 3, length: 3, chamferRadius: 0.5)
        cubeNode.geometry = cubeGeometry
        cubeNode.name = "cube"
        scene.rootNode.addChildNode(cubeNode)
    }
}



#Preview {
    ContentView()
}
