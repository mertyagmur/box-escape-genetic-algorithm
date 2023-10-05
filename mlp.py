import numpy as np

class MLP:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Initialize weights with random values
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        
        # Initialize biases with zeros
        self.bias_hidden = np.zeros((hidden_size, 1))
        self.bias_output = np.zeros((output_size, 1))
        
    def forward(self, input_data):
        # Calculate hidden layer activations
        """ print(input_data.shape)
        print(self.weights_input_hidden.shape)
        print(self.weights_hidden_output.shape) """
        hidden_activations = np.dot(input_data, self.weights_input_hidden) #+ self.bias_hidden
        hidden_outputs = self._sigmoid(hidden_activations)
        
        # Calculate output layer activations
        output_activations = np.dot(hidden_outputs, self.weights_hidden_output)# + self.bias_output
        output = self._sigmoid(output_activations)
        
        return output
    
    def _sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))
